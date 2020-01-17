from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import pyparsing
from contextlib import redirect_stdout
from io import StringIO

from gol.rules_parser.rules_parser import parse, webrepr, Rule
from gol.models import Parse, Task

import json
import traceback
from datetime import datetime


@require_http_methods(['POST'])
@login_required()
def parse_rules(request, *args, **kwargs):
    expr = request.body.decode('utf-8')

    try:
        if 'task' in kwargs:
            task = Task.objects.get(id=kwargs['task'])
        else:
            task = None
    except api_server.models.level.Level.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    colors = kwargs['colors'] if 'colors' in kwargs else ''

    parse_obj = Parse(
        user=request.user,
        task=task,
        input_text=expr,
        params=str(kwargs),
    )

    try:
        parsed = parse(expr, colors)
        rules_ = webrepr(parsed)
        parse_obj.report = 'ok'

        if isinstance(parsed, Rule):
            c_stdout = StringIO()
            with redirect_stdout(c_stdout):
                _ = parsed.pretty_print()
            parse_obj.parsed = c_stdout.getvalue()
        else:
            parse_obj.parsed = str(parsed)
    except pyparsing.ParseException as e:
        parse_obj.report = 'Parse error: ' + str(e)
        return HttpResponseBadRequest(str(e))
    except Exception as e:
        exception_str = traceback.format_exc()
        parse_obj.report = exception_str
        print(exception_str, end='')
        return HttpResponseBadRequest(str(e))
    finally:
        parse_obj.save()

    return JsonResponse(rules_)
