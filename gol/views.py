from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from gol.models import Task
from gol.models import Post


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    tasks = {
        task.id: {
            'id': task.id,
            'name': task.name,
            'category': task.category
        }
        for task in Task.objects.all()
    }

    context = {
        'tasks': tasks,
        'posts': (Post.objects.filter(published__lt=timezone.now()).
                  order_by('-published')[:12]),
    }
    return render(request, "index.html", context)


@login_required(login_url='/login')
def automata(request):
    return render(request, "automata.html")


@login_required(login_url='/admin')
def simulation(request):
    return render(request, "simulation.html")
