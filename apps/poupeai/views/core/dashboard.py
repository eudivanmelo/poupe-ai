import re
from django.http import JsonResponse
from django.db.models import Sum
from apps.poupeai.services.gemini import generate_financial_summary, tip
from django.views.generic import TemplateView
from apps.poupeai.mixins import PoupeAIMixin
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

def relatory_view(request):
    accounts = request.user.accounts.all()
    transactions = request.user.transactions.all()
    
    total_income = sum(account.total_income for account in accounts)
    total_expenses = sum(account.total_expense for account in accounts)
    current_balance = total_income - total_expenses
    
    transactions_data = [
        {
            "date": transaction.payment_at,
            "description": transaction.description,
            "category": transaction.category,
            "amount": transaction.installments_total_amount if transaction.type == 'card' else transaction.amount,
            "type": transaction.type,
        }
        for transaction in transactions
    ]
    
    highest_expense_category = transactions.filter(category__type='expense') \
                                          .values('category') \
                                          .annotate(total_spent=Sum('amount')) \
                                          .order_by('-total_spent') \
                                          .first()

    category_percentage = highest_expense_category['total_spent'] / total_expenses * 100
                                    
    
    prompt_data = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance,
        "transactions": transactions_data,
        "highest_expense_category": request.user.categories.get(id=highest_expense_category['category']),
        "total_category_expense": highest_expense_category['total_spent'],
        "category_percentage": category_percentage,
    }
    
    response = generate_financial_summary(prompt_data)
    return JsonResponse({'success': True, 'message': re.sub(r"```html|```", "", response).strip()})

def tip_view(request):
    accounts = request.user.accounts.all()
    transactions = request.user.transactions.all()
    
    total_income = sum(account.total_income for account in accounts)
    total_expenses = sum(account.total_expense for account in accounts)
    current_balance = total_income - total_expenses
    
    transactions_data = [
        {
            "date": transaction.payment_at,
            "description": transaction.description,
            "category": transaction.category,
            "amount": transaction.installments_total_amount if transaction.type == 'card' else transaction.amount,
            "type": transaction.type,
        }
        for transaction in transactions
    ]
    
    prompt_data = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "current_balance": current_balance,
        "transactions": transactions_data,
    }
    
    response = tip(prompt_data)
    return JsonResponse({'success': True, 'message': re.sub(r"```html|```", "", response).strip()})
    
    
    
    



