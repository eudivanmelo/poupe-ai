from django.views.generic import ListView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, UpdateJsonView
from apps.poupeai.models import CreditCard, Invoice
from django.db.models import Prefetch
from django.utils.timezone import now
from apps.poupeai.forms import CreditCardForm

class CreditCardsListView(PoupeAIMixin, ListView):
    '''
    View for listing all credit cards
    '''

    template_name = 'poupeai/credit_cards_page.html'
    context_object_name = 'credit_cards'

    def get_name(self):
        return "credit-cards"
    
    def get_breadcrumbs(self):
        return [
            {"name": "Dashboard", "url": reverse_lazy('dashboard')},
            {"name": "Cartões de Crédito", "url": None},
        ]

    def get_queryset(self):
        # Obter mês e ano atuais
        month = now().month
        year = now().year

        # Criar um filtro de faturas para o mês e ano atuais
        invoice_filter = Prefetch(
            'invoices', 
            queryset=Invoice.objects.filter(month=month, year=year),
            to_attr='filtered_invoices'  # Salvar as faturas filtradas no atributo 'filtered_invoices'
        )

        # Filtrando cartões de crédito e aplicando o prefetch das faturas
        queryset = CreditCard.objects.all().order_by('created_at').prefetch_related(invoice_filter)

        return queryset

class CreditCardCreateView(CreateJsonView):
    '''
    View for creating a new credit card
    '''
    success_url = reverse_lazy('credit-cards')
    model = CreditCard
    form_class = CreditCardForm
    success_message = 'Cartão de Crédito criado com sucesso!'
    error_message = 'Ocorreu um erro ao criar o cartão de crédito, verifique as informações ou tente novamente mais tarde.'

class CreditCardDeleteView(DeleteJsonView):
    '''
    View for deleting an credit card
    '''
    success_url = reverse_lazy('credit-cards')
    model = CreditCard
    success_message = 'Cartão de Crédito deletado com sucesso!'
    error_message = 'Ocorreu um erro ao deletar o cartão de crédito, verifique as informações ou tente novamente mais tarde.'

class CreditCardUpdateView(UpdateJsonView):
    '''
    View for updating an credit card
    '''
    model = CreditCard
    form_class = CreditCardForm
    success_url = reverse_lazy('credit-cards')
    context_object_name = 'credit_card'
    success_message = 'Cartão de crédito atualizado com sucesso!'
    error_message = 'Ocorreu um erro ao atualizar o cartão de crédito, verifique as informações ou tente novamente mais tarde.'