from django.db import models


class TaskCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128)
    order = models.IntegerField(unique=True, default=0)


class Task(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(default='', max_length=128)
    category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)
    max_points = models.PositiveIntegerField(default=1)
    intro_text = models.TextField(default='')
    config = models.TextField(default='{}')

    def __str__(self):
        return str(self.id)
