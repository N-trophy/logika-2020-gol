from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from gol.rules_parser.rules import rules
from gol.rules_parser.errors import EInvalidExpr

import json
import traceback
from datetime import datetime


@require_http_methods(['POST'])
@login_required()
def parse_rules(request, *args, **kwargs):
    expr = request.body.decode('utf-8')

    try:
        rules_ = rules(expr).repr()
    except EInvalidExpr as e:
        return HttpResponseBadRequest(str(e))

    return JsonResponse(rules_)
