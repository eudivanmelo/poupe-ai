from django.shortcuts import render
from django.urls import reverse_lazy

def help_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Ajuda e Suporte", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "help"}
    return render(request, 'help.html', context)