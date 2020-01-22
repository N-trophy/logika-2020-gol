from django.db import models
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
    rules = models.TextField(default='')
    grid = models.TextField(default='')

    ok = models.BooleanField(default=False)
    int_status = models.CharField(default='', max_length=64)
    points = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    int_report = models.TextField(default='')
    user_report = models.TextField(default='')

    datetime = models.DateTimeField(default=timezone.now)
