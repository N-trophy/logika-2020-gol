from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

from gol.models import Task
from gol.models import Post


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    tasks = [
        {
            'id': task.id,
            'name': task.name,
            'category': task.category
        }
        for task in Task.objects.all()
    ]

    categories = []
    for task in tasks:
        if not task['category'] in categories:
            categories.append(task['category'])

    context = {
        'categories': categories,
        'tasks': tasks,
        'posts': (Post.objects.filter(published__lt=timezone.now()).
                  order_by('-published')[:12]),
    }
    return render(request, "index.html", context)


@login_required(login_url='/admin')
def simulation(request):
    return render(request, "simulation.html")
