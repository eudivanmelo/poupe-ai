from django.shortcuts import render
from django.urls import reverse_lazy

def accounts_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Contas", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "accounts"}
    return render(request, 'poupeai/accounts_page.html', context)