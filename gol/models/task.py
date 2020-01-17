from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Task(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(default='', max_length=128)
    max_points = models.PositiveIntegerField(default=1)
    intro_text = models.TextField(default='')
    config = models.TextField(default='{}')

    def __str__(self):
        return str(self.id)
