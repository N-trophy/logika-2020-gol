from django.http import JsonResponse, HttpResponseBadRequest, \
        HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import traceback
import json

from gol.models import Submission, Task
from gol.models.submission import no_submissions, submissions_remaining
from gol.common import Reporter, Grid, QUALIFICATION_END
import gol.evaluators as evaluators


@require_http_methods(['POST'])
@login_required()
def submit(request, *args, **kwargs):
    data = json.loads(request.body.decode('utf-8'))
    rules = data['rules']
    grid = data['grid']

    if timezone.now() >= QUALIFICATION_END and not request.user.is_superuser:
        return HttpResponseForbidden('Qualification ended!')

    try:
        task = Task.objects.get(id=kwargs['id'])
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    if not hasattr(evaluators, task.eval_function):
        return HttpResponseNotFound('Evaluator not found!')

    done_evaluations = no_submissions(request.user, task)
    if (task.max_submissions > 0 and done_evaluations >= task.max_submissions
            and not request.user.is_superuser):
        return HttpResponseForbidden('Reached limit of submissions!')

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
        ok, score = eval_function(
            task, rules, Grid.fromstr(grid), int_reporter, user_reporter
        )

        submission.ok = ok
        submission.int_status = 'ok'
        submission.score = score
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
        'report': user_reporter.webrepr(),
        'submissions_remaining': submissions_remaining(request.user, task),
    })
