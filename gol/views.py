from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from gol.models import Task, Post, TaskCategory


@login_required(login_url='/admin')
def simulation(request):
    return render(request, "simulation.html")


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    context = {
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

    context = {
        'task': task,
    }
    return render(request, "task.html", context)
