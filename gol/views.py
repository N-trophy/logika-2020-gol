from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required


def index(request, *args, **kwargs):
    return render(request, "index.html")


@login_required(login_url='/admin')
def automata(request):
    return render(request, "automata.html")
