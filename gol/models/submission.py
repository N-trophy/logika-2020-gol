from typing import Dict, Optional, List
from django.db import models
from django.db.models import Max
from django.contrib.auth.models import User
from django.utils import timezone

from gol.models.task import Task


class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    rules = models.TextField(default='', blank=True)
    grid = models.TextField(default='', blank=True)

    ok = models.BooleanField(default=False)
    int_status = models.CharField(default='', max_length=64, blank=True)
    score = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    int_report = models.TextField(default='', blank=True)
    user_report = models.TextField(default='', blank=True)

    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)


def no_submissions(user: User, task: Task):
    return Submission.objects.filter(user=user, task=task).count()


def submissions_remaining(user: User, task: Task):
    if task.max_submissions == 0 or user.is_superuser:
        return -1
    return task.max_submissions - no_submissions(user, task)


def submitted_ok(user: User) -> Dict[int, bool]:
    return {
        res['task']: res['ok']
        for res in Submission.objects.filter(user=user).
                   values('task').annotate(ok=Max('ok'))
    }


def best_submission(user: User, task: Task) -> Submission:
    request = Submission.objects.filter(user=user, ok=True, task=task)
    if task.best_score_func.lower() == 'min':
        return request.order_by('score', '-datetime').first()
    elif task.best_score_func.lower() == 'max':
        return request.order_by('-score', '-datetime').first()
    else:
        return None


def best_submissions(user: User, tasks: Optional[List[Task]] = None) \
        -> Dict[Task, Submission]:
    result = {}
    if tasks is None:
        tasks = Task.objects.all()
    submissions = Submission.objects.filter(user=user).all()

    submissions_dict = {}
    for submission in submissions:
        if submission.task not in submissions_dict:
            submissions_dict[submission.task] = []
        submissions_dict[submission.task].append(submission)

    for task in tasks:
        task_submissions = submissions_dict[task] \
            if task in submissions_dict else []

        if task.best_score_func.lower() == 'min':
            result[task] = max(
                task_submissions,
                key=lambda subm: (subm.ok, -subm.score, subm.datetime),
                default=None
            )
        elif task.best_score_func.lower() == 'max':
            result[task] = max(
                task_submissions,
                key=lambda subm: (subm.ok, subm.score, subm.datetime),
                default=None
            )
        else:
            result[task] = max(
                task_submissions, key=lambda subm: (subm.ok, subm.datetime),
                default=None
            )

    return result
