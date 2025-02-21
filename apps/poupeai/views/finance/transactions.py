from django.shortcuts import render
from django.views.generic import ListView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models import Transaction
from apps.poupeai.forms import TransactionForm
from apps.poupeai.views.generic.json import DeleteJsonView, DetailJsonView, CreateJsonView, UpdateJsonView
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['credit_cards'] = self.request.user.credit_cards.all()
        context['accounts'] = self.request.user.accounts.all()
        context['categories'] = self.request.user.categories.all()
        
        return context
        
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
            data['credit_card'] = obj.card_transactions.first().credit_card.name
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
    
class TransactionCreateView(CreateJsonView):
    '''
    View to create a transaction
    '''
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transactions')
    success_message = "Transação criada com sucesso!"
    error_message = "Erro ao criar transação!"
    
class TransactionUpdateView(UpdateJsonView):
    model = Transaction
    context_object_name = 'transaction'
    form_class = TransactionForm
    success_url = reverse_lazy('transactions')
    success_message = "Transação atualizada com sucesso!"
    error_message = "Erro ao atualizar transação!"
    
    def get_object_data(self, obj):
        data = super().get_object_data(obj)

        data['attachment'] = obj.attachment.url if obj.attachment else None
        data['category'] = obj.category.id
        
        if obj.type == 'card':
            data['credit_card'] = obj.card_transactions.first().credit_card.id
            data['installments'] = obj.card_transactions.count()
        else:
            data['account'] = obj.account_transaction.account.id
            data['expire_at'] = obj.account_transaction.expire_at
        
        return data
    
    