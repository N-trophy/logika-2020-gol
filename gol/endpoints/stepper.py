from django.http import JsonResponse, HttpResponseBadRequest, \
        HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import traceback
import json

from gol.common import Grid
from gol.models import Task
import gol.steppers as steppers


@require_http_methods(['POST'])
@login_required()
def step(request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    grid = data['grid']

    try:
        task = Task.objects.get(id=kwargs['id'])
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    if not task.stepper_function:
        return HttpResponseBadRequest('This task does not support stepping!')

    if not hasattr(steppers, task.stepper_function):
        return HttpResponseNotFound('Evaluator not found!')

    step_function = getattr(steppers, task.stepper_function)

    try:
        new_grid = step_function(task, Grid.fromstr(grid))
    except Exception:
        exception_str = traceback.format_exc()
        print(exception_str, end='')
        return HttpResponseBadRequest('Vnitřní výjimka vyhodnocovátka, '
                                      'kontaktujte organizátory!')

    return JsonResponse({
        'grid': new_grid.webrepr(),
    })
