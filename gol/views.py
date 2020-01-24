from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import re

from gol.models import Task, Post, TaskCategory
from gol.models.submission import submissions_remaining


@login_required(login_url='/login')
def simulation(request):
    context = {
        'user': request.user,
    }
    return render(request, "simulation.html", context)


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    context = {
        'user': request.user,
        'categories': TaskCategory.objects.order_by('order').all(),
        'tasks': Task.objects.order_by('id').all(),
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

    task.start_config = task.start_config.replace("\r\n", "\\n")

    task.should_submit = True

    context = {
        'user': request.user,
        'task': task,
        'remaining_submissions': submissions_remaining(request.user, task),
    }
    return render(request, "task.html", context)
