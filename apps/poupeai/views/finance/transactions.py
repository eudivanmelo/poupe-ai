from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Transaction
from apps.poupeai.forms import TransactionForm
from apps.poupeai.views.generic.json import DeleteJsonView, DetailJsonView, CreateJsonView
from django.db.models import Q
from django.forms.models import model_to_dict


class TransactionsListView(PoupeAIMixin, ListView):
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
        queryset = Transaction.objects.filter(user=self.request.user).prefetch_related("card_transactions", "account_transaction").order_by("-created_at")
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(category__name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(amount__icontains=search_query)
            )
        return queryset
    
class TransactionDetailView(DetailJsonView):
    model = Transaction
    context_object_name = 'transaction'
    fields = ['description', 'amount', 'created_at', 'type', 'status', 'payment_at']
    
    def get_object_data(self, obj):
        data = super().get_object_data(obj)
        
        data['image'] = obj.attachment.url if obj.attachment else None
        data['category'] = obj.category.name
        
        if obj.type == 'card':
            data['card_transaction'] = [model_to_dict(ct) for ct in obj.card_transactions.all()]
            data['installments_total_amount'] = obj.installments_total_amount
            data['total_installments'] = obj.total_installments
        else:
            data['account_transaction'] = model_to_dict(obj.account_transaction)
            data['account_transaction']['account'] = obj.account_transaction.account.name
        
        return data
    
class TransactionDeleteView(DeleteJsonView):
    '''
    View to delete a transaction
    '''
    model = Transaction
    success_url = reverse_lazy('transactions')
    success_message = "Transação excluída com sucesso!"
    error_message = "Erro ao excluir transação!"
    
class TestCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "poupeai/test.html"
    success_url = reverse_lazy('transactions')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TransactionCreateView(CreateJsonView):
    '''
    View to create a transaction
    '''
    model = Transaction
    form_class = TransactionForm
    fields = ['description', 'amount', 'type', 'category', 'status', 'attachment']
    success_url = reverse_lazy('transactions')
    success_message = "Transação criada com sucesso!"
    error_message = "Erro ao criar transação!"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)