from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView
from apps.poupeai.models import Account
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, DetailJsonView, UpdateJsonView
from django.forms.models import model_to_dict

class AccountsListView(PoupeAIMixin, ListView):
    '''
    View for listing all accounts
    '''
    
    template_name = 'poupeai/accounts_page.html'
    context_object_name = 'accounts'
    queryset = Account.objects.all().order_by('created_at')
    paginate_by = 10
    
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Account.objects.all().order_by('created_at')
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["balance_total"] = sum([account.balance for account in context['accounts']])
        context["total_income"] = sum([account.total_income for account in context['accounts']])
        context["total_expense"] = sum([account.total_expense for account in context['accounts']])
        return context
    
    
class AccountCreateView(CreateJsonView):
    '''
    View for creating a new account
    '''
    success_url = reverse_lazy('accounts')
    model = Account
    fields = ['name', 'description', 'balance']
    success_message = 'Conta criada com sucesso!'
    error_message = 'Ocorreu um erro ao criar a conta, verifique as informações ou tente novamente mais tarde.'
    
    
class AccountDeleteView(DeleteJsonView):
    '''
    View for deleting an account
    '''
    success_url = reverse_lazy('accounts')
    model = Account
    success_message = 'Conta deletada com sucesso!'
    error_message = 'Ocorreu um erro ao deletar a conta, verifique as informações ou tente novamente mais tarde.'
    

class AccountDetailView(DetailJsonView):
    '''
    View for returning the account details
    '''
    model = Account
    context_object_name = 'account'
    fields = ['name', 'description', 'balance', 'total_income', 'total_expense', 'created_at']
    
    def get_object_data(self, obj):
        data = super().get_object_data(obj)
        
        transactions = obj.account_transactions.all().order_by('-transaction__created_at')[:10]
        data['transactions'] = [
        {
            'amount': transaction.transaction.amount,
            'type': transaction.type,
            'description': transaction.transaction.description,
            'created_at': transaction.transaction.created_at
        }
        for transaction in transactions
        ]
        
        return data
    

class AccountUpdateView(UpdateJsonView):
    '''
    View for updating an account
    '''
    model = Account
    fields = ['name', 'description']
    success_url = reverse_lazy('accounts')
    context_object_name = 'account'
    success_message = 'Conta atualizada com sucesso!'
    error_message = 'Ocorreu um erro ao atualizar a conta, verifique as informações ou tente novamente mais tarde.'


