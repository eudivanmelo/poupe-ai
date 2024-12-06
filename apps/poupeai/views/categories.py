from django.shortcuts import render
from django.urls import reverse_lazy

def categories_view(request):
    breadcrumbs = [
        {"name":"Dashboard", "url": reverse_lazy('dashboard')},
        {"name":"Categorias", "url": None},
    ]
    context = {"breadcrumbs": breadcrumbs, "name" : "categories"}
    return render(request, 'categories.html', context)