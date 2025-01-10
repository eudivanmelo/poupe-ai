from django.shortcuts import render
from django.urls import reverse_lazy

def profile_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Perfil", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "profile"}
    return render(request, 'profile.html', context)