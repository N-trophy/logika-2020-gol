from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import pyparsing

from gol.rules_parser.rules_parser import parse, webrepr

import json
import traceback
from datetime import datetime


@require_http_methods(['POST'])
@login_required()
def parse_rules(request, *args, **kwargs):
    expr = request.body.decode('utf-8')

    try:
        rules_ = webrepr(parse(expr))
    except pyparsing.ParseException as e:
        return HttpResponseBadRequest(str(e))

    # TODO: log other exceptions

    return JsonResponse(rules_)
