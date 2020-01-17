from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required


@login_required(login_url='/login')
def index(request, *args, **kwargs):
    return render(request, "index.html")


@login_required(login_url='/login')
def automata(request):
    return render(request, "automata.html")


@login_required(login_url='/admin')
def simulation(request):
    return render(request, "simulation.html")