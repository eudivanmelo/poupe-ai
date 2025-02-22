from django.views.generic import TemplateView
from apps.poupeai.mixins import PoupeAIMixin
from django.db.models import Sum
from django.utils.timezone import now

class DashboardView(PoupeAIMixin, TemplateView):
    template_name = 'poupeai/dashboard.html'

    def get_context_data(self, **kwargs):
        current_month_start = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        context = super().get_context_data(**kwargs)
        context['credit_cards'] = self.request.user.credit_cards.all()
        context['accounts'] = self.request.user.accounts.all()
        context["balance_total"] = sum([account.balance for account in context['accounts']])

        context["total_income_month"] = sum([
            account.account_transactions.filter(
                transaction__category__type='income',
                transaction__created_at__range=(current_month_start, current_month_end)
            ).aggregate(total=Sum('transaction__amount'))['total'] or 0
            for account in context['accounts']
        ])

        # Calcula o total de despesas (saídas) mensais
        context["total_expense_month"] = sum([
            account.account_transactions.filter(
                transaction__category__type='expense',
                transaction__created_at__range=(current_month_start, current_month_end)
            ).aggregate(total=Sum('transaction__amount'))['total'] or 0
            for account in context['accounts']
])
        
        context['categories'] = self.request.user.categories.all()
        context['transactions'] = self.request.user.transactions.all()
       
        
        return context