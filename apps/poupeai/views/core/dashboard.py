import re
from django.http import JsonResponse
from django.db.models import Sum
from apps.poupeai.services.gemini import generate_financial_summary, tip
from django.views.generic import TemplateView
from apps.poupeai.mixins import PoupeAIMixin
from django.utils.timezone import now
from apps.poupeai.utils import generate_color
from datetime import datetime, date


class DashboardView(PoupeAIMixin, TemplateView):
    template_name = 'poupeai/dashboard.html'

    def get_context_data(self, **kwargs):
        current_month_start = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_month_end = now().replace(hour=23, minute=59, second=59, microsecond=999999)
        current_month = date.today().month
        current_year = date.today().year
    
        
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
        
    # Calcula o total das faturas fechadas mas não pagas
        total_closed_unpaid_invoices = sum([
        invoice.balance_due for credit_card in context['credit_cards'] for invoice in credit_card.invoices.filter(
                paid=False,
                month__lte=current_month,
                year=current_year
            )
            if invoice.status == 'closed'  # Verificação do status da fatura
        ])
        context["total_closed_unpaid_invoices"] = total_closed_unpaid_invoices
    
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

def category_chart_data(request):
    categories = request.user.categories.all()
    
    data = {
        "labels": [],
        "datasets": [
            {
                "data": [],
                "backgroundColor": [],
                "borderWidth": 0,
            }
        ]
    }
    
    for category in categories:
        total_value = category.total_transactions_value
        if total_value > 0:
            data["labels"].append(category.name)
            data["datasets"][0]["data"].append(float(total_value))
            data["datasets"][0]["backgroundColor"].append(category.color)
    
    return JsonResponse(data)

def cards_analytics_chart_data(request):
    credit_cards = request.user.credit_cards.all()
    
    data = {
        "labels": [],
        "datasets": [
            {
                "label": "Limite",
                "backgroundColor": "rgb(25, 32, 52)",
                "borderColor": "rgb(25, 32, 52)",
                "data": [],
            },
            {
                "label": "Gastos",
                "backgroundColor": "rgb(250, 80, 7)",
                "borderColor": "rgb(250, 80, 7)",
                "data": [],
            },
        ],
    }

    for card in credit_cards:
        data["labels"].append(card.name)
        data["datasets"][0]["data"].append(float(card.limit))  # Limite do cartão
        data["datasets"][1]["data"].append(float(card.outstanding))  # Gastos pendentes

    return JsonResponse(data)

def balance_analytics_chart_data(request):
    user = request.user
    accounts = user.accounts.all()
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    datasets = []
    for i, account in enumerate(accounts):
        monthly_balances = []
        for month in range(1, 13):
            transactions = account.account_transactions.filter(
                expire_at__month=month, expire_at__year=datetime.now().year
            )
            
            total_income = transactions.filter(transaction__category__type='income').aggregate(Sum('transaction__amount'))['transaction__amount__sum'] or 0
            total_expense = transactions.filter(transaction__category__type='expense').aggregate(Sum('transaction__amount'))['transaction__amount__sum'] or 0
            monthly_balance = float(total_income) - float(total_expense)

            monthly_balances.append(monthly_balance)

        datasets.append({
            "label": account.name,
            "borderColor": generate_color(i),
            "pointBorderColor": "#FFF",
            "pointBackgroundColor": generate_color(i),
            "pointBorderWidth": 2,
            "pointHoverRadius": 4,
            "pointHoverBorderWidth": 1,
            "pointRadius": 4,
            "backgroundColor": generate_color(i) + "aa",
            "fill": True,
            "borderWidth": 2,
            "data": monthly_balances,
        })

    data = {
        "labels": months,
        "datasets": datasets
    }

    return JsonResponse(data)
    
    
    



