from django.shortcuts import render
from django.urls import reverse_lazy

def creditcard_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Cartões de Crédito", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "credit-card"}
    return render(request, 'credit-card.html', context)