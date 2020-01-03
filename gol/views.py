from django.shortcuts import render


def automata_view(request):
    return render(request, "automata.html")