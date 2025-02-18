from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin

class TransactionsView(PoupeAIMixin, TemplateView):
    template_name = "poupeai/transactions_page.html"

    def get_name(self):
        return "transactions"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Transações", "url": None},
        ]