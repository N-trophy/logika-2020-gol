from django.http import JsonResponse, HttpResponseBadRequest, \
        HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import pyparsing
from contextlib import redirect_stdout
from io import StringIO
import time

from gol.rules_parser.rules_parser import parse, webrepr, Rule, \
    nicer_parse_error_message
from gol.models import Parse, Task

import traceback


@require_http_methods(['POST'])
@login_required()
def parse_rules(request, *args, **kwargs):
    expr = request.body.decode('utf-8')

    try:
        if 'task' in kwargs:
            task = Task.objects.get(id=kwargs['task'])
        else:
            task = None
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    colors = kwargs['colors'] if 'colors' in kwargs else 'rgbk'
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
        parse_obj.report = str(e) + '\n\n' + nicer_msg
        return HttpResponseBadRequest(nicer_msg)
    except Exception as e:
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
