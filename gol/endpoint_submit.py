from django.http import JsonResponse, HttpResponseBadRequest, \
        HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import traceback
import json

from gol.models import Submission, Task
from gol.common import Reporter
import gol.evaluators as evaluators


@require_http_methods(['POST'])
@login_required()
def submit(request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    rules = data['rules']
    grid = data['grid']

    try:
        task = Task.objects.get(id=kwargs['id'])
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    if not hasattr(evaluators, task.eval_function):
        return HttpResponseNotFound('Evaluator not found!')

    submission = Submission(
        user=request.user,
        task=task,
        rules=rules,
        grid=grid,
    )

    int_reporter = Reporter()
    user_reporter = Reporter()
    eval_function = getattr(evaluators, task.eval_function)

    try:
        ok, points = eval_function(
            task, rules, grid, user_reporter, int_reporter
        )

        submission.ok = ok
        submission.int_status = 'ok'
        submission.points = points
        submission.int_report = int_reporter.text()
        submission.user_report = user_reporter.text()
    except Exception:
        exception_str = traceback.format_exc()
        submission.ok = False
        submission.int_report = exception_str + '\n\n' + int_reporter.text()
        submission.int_status = 'exception'
        print(exception_str, end='')
        return HttpResponseBadRequest('Vnitřní výjimka vyhodnocovátka, '
                                      'kontaktujte organizátory!')
    finally:
        submission.save()

    return JsonResponse({
        'ok': ok,
        'points': points,
        'report': user_reporter.text(),
    })
