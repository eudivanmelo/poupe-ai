from django.shortcuts import render
from django.urls import reverse_lazy

def profile_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Perfil", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "profile"}
    return render(request, 'poupeai/profile_page.html', context)

def profile_deletion_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Perfil", "url": reverse_lazy('profile')},
        {"name":"Solicitar Exclusão de Conta", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "account-deletion"}
    return render(request, 'poupeai/account_deletion.html', context)