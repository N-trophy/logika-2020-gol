from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import re

from gol.models import Task, Post, TaskCategory
from gol.models.submission import submissions_remaining, submitted_ok


@login_required(login_url='/login')
def simulation(request):
    context = {
        'user': request.user,
    }
    return render(request, "simulation.html", context)


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    tasks = Task.objects.order_by('id').all()
    submitted = submitted_ok(request.user)
    for task in tasks:
        if task.id in submitted:
            task.submitted = 'ok' if submitted[task.id] else 'nok'
        else:
            task.submitted = 'no'

    context = {
        'user': request.user,
        'categories': TaskCategory.objects.order_by('order').all(),
        'tasks': tasks,
        'posts': (Post.objects.filter(published__lt=timezone.now()).
                  order_by('-published')[:12]),
    }
    return render(request, "index.html", context)


@login_required(login_url='/login')
def task(request, *args, **kwargs):
    try:
        task = Task.objects.get(id=kwargs['id'])
    except Task.DoesNotExist:
        return HttpResponseNotFound('Task not found')

    if not task.rules_public:
        task.rules = ''  # prevent security vulnerabilities in template

    task.allowed_colors = task.allowed_colors.lower()
    task.start_config = task.start_config.replace("\r\n", "\\n")

    task.should_submit = True

    context = {
        'user': request.user,
        'task': task,
        'remaining_submissions': submissions_remaining(request.user, task),
    }
    return render(request, "task.html", context)


@login_required(login_url='/login')
def help(request, *args, **kwargs):
    return render(request, "help.html")
