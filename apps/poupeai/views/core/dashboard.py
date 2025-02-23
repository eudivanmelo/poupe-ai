from django.http import HttpResponse
from django.db.models import Sum
from apps.poupeai.services.gemini import generate_financial_summary
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
    return HttpResponse(response)
    



