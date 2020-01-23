from django.db import models


class TaskCategory(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=128)
    order = models.IntegerField(unique=True, default=0)


class Task(models.Model):
    GRID_TYPE = [('PLANE', 'plane'), ('TORUS', 'torus')]

    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=128)
    category = models.ForeignKey(TaskCategory, on_delete=models.PROTECT)
    max_points = models.PositiveIntegerField(default=1)
    intro_text = models.TextField(default='')

    grid_type = models.CharField(max_length=16, choices=GRID_TYPE, default='PLANE')
    klikatko = models.BooleanField(default=True)
    klikatko_width = models.IntegerField(default=25)
    klikatko_height = models.IntegerField(default=25)
    allowed_colors = models.CharField(default='rgbk', max_length=64)
    start_config = models.TextField(default='', blank=True)
    rules = models.TextField(default='', blank=True)
    rules_public = models.BooleanField(default=False)
    eval_function = models.CharField(default='func_name', max_length=128,
                                     blank=True)
    stepper_function = models.CharField(default='', max_length=128,
                                        blank=True)
    max_submissions = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def is_stepper(self) -> bool:
        return self.stepper_function != ''
