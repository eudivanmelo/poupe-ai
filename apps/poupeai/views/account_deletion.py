from django.shortcuts import render
from django.urls import reverse_lazy

def account_deletion_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Perfil", "url": reverse_lazy('profile')},
        {"name":"Solicitar Exclusão de Conta", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "account-deletion"}
    return render(request, 'account-deletion.html', context)