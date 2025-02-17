from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.poupeai.models import Account
from apps.poupeai.mixins import BreadcrumbMixin, PageNameMixin

class AccountsListView(LoginRequiredMixin, ListView, BreadcrumbMixin, PageNameMixin):
    '''
    View for listing all accounts
    '''
    
    template_name = 'accounts.html'
    context_object_name = 'accounts'
    queryset = Account.objects.all()
    
class AccountCreateView(LoginRequiredMixin):
    '''
    View for creating a new account
    '''
    success_url = reverse_lazy('poupeai:accounts')
    
    