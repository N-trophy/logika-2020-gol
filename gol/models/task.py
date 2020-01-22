from django.db import models


class TaskCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128)
    order = models.IntegerField(unique=True, default=0)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=128)
    category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)
    max_points = models.PositiveIntegerField(default=1)
    intro_text = models.TextField(default='')

    klikatko = models.BooleanField(default=True)
    klikatko_width = models.IntegerField(default=25)
    klikatko_height = models.IntegerField(default=25)
    allowed_colors = models.CharField(default='rgbk', max_length=64)
    start_config = models.TextField(default='')
    rules = models.TextField(default='')
    rules_public = models.BooleanField(default=False)
    eval_function = models.CharField(default='func_name', max_length=128)
    max_evaluations = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)
