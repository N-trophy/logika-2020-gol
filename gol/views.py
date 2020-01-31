from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.models import User

from gol.models import Task, Post, TaskCategory
from gol.models.submission import submissions_remaining, submitted_ok, \
        best_submission, best_submissions


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
        if task.should_submit():
            if task.id in submitted:
                task.submitted = 'ok' if submitted[task.id] else 'nok'
                task.best_submission = best_submission(request.user, task)
            else:
                task.submitted = 'no'
        else:
            task.submitted = 'not'

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
    task.best_submission = best_submission(request.user, task)

    context = {
        'user': request.user,
        'task': task,
        'remaining_submissions': submissions_remaining(request.user, task),
    }
    return render(request, "task.html", context)


@login_required(login_url='/login')
def help(request, *args, **kwargs):
    return render(request, "help.html")


@login_required(login_url='/login')
@user_passes_test(lambda u: u.is_superuser)
def monitor(request, *args, **kwargs):
    tasks = Task.objects.exclude(eval_function__exact='').all()
    users = list(User.objects.filter(id__gte=20).all())
    for user in users:
        user.best_submissions = best_submissions(user, tasks=tasks).values()

    users.sort(key=lambda u: len(
        list(filter(lambda subm: subm is not None, u.best_submissions))
    ), reverse=True)

    context = {
        'user': request.user,
        'tasks': tasks,
        'users': users,
    }
    return render(request, "monitor.html", context)
