from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.urls import reverse_lazy
from apps.poupeai.mixins import PoupeAIMixin
from apps.poupeai.models.account import Account
from apps.poupeai.views.generic.json import CreateJsonView, DeleteJsonView, UpdateJsonView
from apps.poupeai.models import CreditCard, Invoice, Transaction
from django.db.models import Prefetch
from django.utils.timezone import now
from datetime import date
from apps.poupeai.forms import CreditCardForm, InvoicePaymentForm

class CreditCardsListView(PoupeAIMixin, ListView):
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
        # Obter mês e ano da requisição ou usar o mês e ano atuais
        month = int(self.request.GET.get('month', now().month))
        year = int(self.request.GET.get('year', now().year))

        # Criar um filtro de faturas para o mês e ano selecionados
        invoice_filter = Prefetch(
            'invoices', 
            queryset=Invoice.objects.filter(month=month, year=year),
            to_attr='filtered_invoices'
        )

        # Filtrando cartões de crédito e aplicando o prefetch das faturas
        queryset = CreditCard.objects.all().filter(user=self.request.user).order_by('created_at').prefetch_related(invoice_filter)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = self.request.user.accounts.all()
        context['categories'] = self.request.user.categories.all()

        # Adicionar meses e anos para o formulário de filtragem
        context['months'] = [
            {'value': 1, 'name': 'Janeiro'}, {'value': 2, 'name': 'Fevereiro'},
            {'value': 3, 'name': 'Março'}, {'value': 4, 'name': 'Abril'},
            {'value': 5, 'name': 'Maio'}, {'value': 6, 'name': 'Junho'},
            {'value': 7, 'name': 'Julho'}, {'value': 8, 'name': 'Agosto'},
            {'value': 9, 'name': 'Setembro'}, {'value': 10, 'name': 'Outubro'},
            {'value': 11, 'name': 'Novembro'}, {'value': 12, 'name': 'Dezembro'},
        ]
        context['years'] = range(now().year - 5, now().year + 5)  # Últimos 5 anos e o atual
        context['selected_month'] = int(self.request.GET.get('month', now().month))
        context['selected_year'] = int(self.request.GET.get('year', now().year))

        return context

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

class InvoicePaymentView(CreateJsonView):
    model = Transaction
    form_class = InvoicePaymentForm
    template_name = 'credit-cards.html'  # Template onde o modal está inserido
    success_url = reverse_lazy('credit_cards')  # Redirecionar para a lista de cartões após o sucesso
    success_message = "Pagamento registrado com sucesso!"
    error_message = "Erro ao registrar pagamento!"

    def form_valid(self, form):
        invoice = get_object_or_404(Invoice, id=self.kwargs['pk'])
        
        # Salva o formulário manualmente e evita a chamada duplicada
        transaction = form.save(invoice=invoice, user=self.request.user)
        
        # Define o objeto salvo para a classe genérica
        self.object = transaction
        
        # Retorna a resposta JSON ou HTTP
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'id': self.object.id, 'message': self.success_message})
        return HttpResponseBadRequest('Requisição inválida')