from django.shortcuts import render
from django.urls import reverse_lazy

def categories_view(request):
    categories_despesas = [
        {"id": 1, "nome": "Aluguel", "valor": 1000.50, "cor": "#ff0000"},
        {"id": 2, "nome": "Supermercado de Arroz", "valor": 500.00, "cor": "#00ff00"},
        {"id": 3, "nome": "Transporte", "valor": 150.00, "cor": "#ff6600"},
        {"id": 4, "nome": "Internet", "valor": 120.00, "cor": "#00ffff"},
        {"id": 5, "nome": "Saúde", "valor": 300.00, "cor": "#ff99cc"},
    ]

    categories_receitas = [
        {"id": 6, "nome": "Salário", "valor": 5000.00, "cor": "#0000ff"},
        {"id": 7, "nome": "Freelance", "valor": 1500.00, "cor": "#00ffcc"},
        {"id": 8, "nome": "Investimentos", "valor": 1000.00, "cor": "#9966ff"},
    ]

    categories_contas = []

    total_cat_despesas = len(categories_despesas)
    total_cat_receitas = len(categories_receitas)
    total_cat_contas = len(categories_contas)

    total_despesas = sum(float(c["valor"]) for c in categories_despesas)
    total_receitas = sum(float(c["valor"]) for c in categories_receitas)
    total_contas = sum(float(c["valor"]) for c in categories_contas)

    breadcrumbs = [
        {"name": "Dashboard", "url": reverse_lazy('dashboard')},
        {"name": "Categorias", "url": None},
    ]

    context = {
        "breadcrumbs": breadcrumbs,
        "categories_despesas": categories_despesas,
        "categories_receitas": categories_receitas,
        "categories_contas": categories_contas,
        "total_despesas": total_despesas,
        "total_receitas": total_receitas,
        "total_contas": total_contas,
        "total_cat_despesas": total_cat_despesas,
        "total_cat_receitas": total_cat_receitas,
        "total_cat_contas": total_cat_contas,
        "name": "categories"
    }
    return render(request, 'categories.html', context)