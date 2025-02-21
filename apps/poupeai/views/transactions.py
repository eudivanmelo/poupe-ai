from django.shortcuts import render
from django.urls import reverse_lazy

def transactions_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Transações", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "transactions"}
    return render(request, 'transactions.html', context)