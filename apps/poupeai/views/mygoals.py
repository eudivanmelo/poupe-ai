from django.shortcuts import render
from django.urls import reverse_lazy

def mygoals_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Minhas Metas", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "my-goals"}
    return render(request, 'my-goals.html', context)