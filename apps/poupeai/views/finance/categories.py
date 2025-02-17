from django.views.generic import TemplateView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin

class CategoriesView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/categories_page.html"

    def get_name(self):
        return "categories"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Categorias", "url": None},
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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

        total_cat_despesas = len(categories_despesas)
        total_cat_receitas = len(categories_receitas)

        total_despesas = sum(float(c["valor"]) for c in categories_despesas)
        total_receitas = sum(float(c["valor"]) for c in categories_receitas)

        context.update({
            "categories_despesas": categories_despesas,
            "categories_receitas": categories_receitas,
            "total_despesas": total_despesas,
            "total_receitas": total_receitas,
            "total_cat_despesas": total_cat_despesas,
            "total_cat_receitas": total_cat_receitas,
        })
        
        return context