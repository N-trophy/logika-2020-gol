from django.http import JsonResponse, HttpResponseBadRequest, \
        HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import pyparsing
from contextlib import redirect_stdout
from io import StringIO
import time
import traceback
import json

from gol.rules_parser.rules_parser import parse, webrepr, Rule, \
    nicer_parse_error_message
from gol.models import Parse, Task


@require_http_methods(['POST'])
@login_required()
def parse_rules(request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    expr = data['expr']
    task_id = data['task'] if 'task' in data else None
    colors = data['colors'] if 'colors' in data else 'rgbk'

    task = None

    try:
        if task_id:
            task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    colors += colors.upper()

    parse_obj = Parse(
        user=request.user,
        task=task,
        input_text=expr,
        params=str(kwargs),
    )

    start = time.time()
    try:
        parsed = parse(expr, colors)
        rules_ = webrepr(parsed)
        parse_obj.state = 'ok'

        if isinstance(parsed, Rule):
            c_stdout = StringIO()
            with redirect_stdout(c_stdout):
                _ = parsed.pretty_print()
            parse_obj.parsed = c_stdout.getvalue()
        else:
            parse_obj.parsed = str(parsed)
    except pyparsing.ParseException as e:
        parse_obj.state = 'parse error'
        nicer_msg = nicer_parse_error_message(str(e))
        parse_obj.report = nicer_msg + '\n\n' + str(e)
        return HttpResponseBadRequest(nicer_msg)
    except Exception:
        exception_str = traceback.format_exc()
        parse_obj.state = 'exception'
        parse_obj.report = exception_str
        print(exception_str, end='')
        return HttpResponseBadRequest('Vnitřní výjimka parsovátka, kontaktujte'
                                      ' organizátory!')
    finally:
        end = time.time()
        parse_obj.evaluation_time = end-start
        parse_obj.save()

    return JsonResponse(rules_)
