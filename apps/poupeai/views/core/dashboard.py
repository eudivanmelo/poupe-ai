from django.shortcuts import render
from django.views.generic import TemplateView
from apps.poupeai.mixins import PoupeAIMixin

class DashboardView(PoupeAIMixin, TemplateView):
    template_name = 'poupeai/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credit_cards'] = self.request.user.credit_cards.all()
        context['accounts'] = self.request.user.accounts.all()
        context['categories'] = self.request.user.categories.all()
        context['transactions'] = self.request.user.transactions.all()
        
        return context