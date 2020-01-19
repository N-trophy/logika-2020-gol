from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from gol.models import Task, Post, TaskCategory


@login_required(login_url='/admin')
def simulation(request):
    context = {
        'name': request.user.get_full_name() if request.user.is_authenticated else 'Anonymní Keporkak',
    }
    return render(request, "simulation.html", context)


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    context = {
        'name': request.user.get_full_name() if request.user.is_authenticated else 'Anonymní Keporkak',
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
        'name': request.user.get_full_name() if request.user.is_authenticated else 'Anonymní Keporkak',
        'task': task,
    }
    return render(request, "task.html", context)
