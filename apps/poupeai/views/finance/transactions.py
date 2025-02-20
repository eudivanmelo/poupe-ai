from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Transaction
from django.db.models import Q


class TransactionsView(PoupeAIMixin, ListView):
    context_object_name = 'transactions'
    template_name = "poupeai/transactions_page.html"
    paginate_by = 10

    def get_name(self):
        return "transactions"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Transações", "url": None},
        ]
        
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user).prefetch_related("card_transaction", "account_transaction").order_by("-created_at")
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(category__name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(amount__icontains=search_query)
            )
        return queryset