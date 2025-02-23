from django import forms
from .models import Transaction, CardTransaction, AccountTransaction
from .models import CreditCard, Account, Invoice, Category
from django.db import transaction
import calendar
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from decimal import Decimal

class TransactionForm(forms.ModelForm):
    TRANSACTION_TYPE_CHOICES = (
        ('card', 'Cartão de Crédito'),
        ('account', 'Conta Bancária'),
    )
    
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Tipo de Transação"
    )
    
    credit_card = forms.ModelChoiceField(
        queryset=CreditCard.objects.all(),
        required=False,
        label="Cartão de Crédito"
    )
    
    installments = forms.IntegerField(
        required=False,
        min_value=1,
        initial=1,
        label="Número de Parcelas",
        help_text="Caso a transação seja parcelada, defina o número de parcelas.",
    )
    
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=False,
        label="Conta"
    )
    
    expire_at = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Vencimento"
    )

    payment_at = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Pagamento"
    )
    
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'category', 'attachment', 'transaction_type', 'credit_card', 'installments', 'account', 'expire_at', 'payment_at']
        
    def clean(self):
        cleaned_data = super().clean()
        
        transaction_type = cleaned_data.get('transaction_type')
        amount = cleaned_data.get('amount')
        num_installments = self.cleaned_data.get("installments")
   
        if transaction_type == 'card':
            credit_card = cleaned_data.get('credit_card')
            payment_at = cleaned_data.get('payment_at')
            
            if not credit_card:
                self.add_error('credit_card', 'Informe o cartão de crédito')
                
            if not payment_at:
                self.add_error('payment_at', 'Informe a data de pagamento')

            # Verifica se o valor da transação excede o limite disponível
            if credit_card and amount:
                if amount * num_installments > credit_card.available:
                    self.add_error('amount', f'O valor da transação excede o limite disponível ({credit_card.available:.2f}).')

        if transaction_type == 'account':
            account = cleaned_data.get('account')
            expire_at = cleaned_data.get('expire_at')
            
            if not account:
                self.add_error('account', 'Informe a conta bancária')
            
            if not expire_at:
                self.add_error('expire_at', 'Informe a data de vencimento')
        
        return cleaned_data
    
    def get_or_create_invoice(self, credit_card, invoice_month, invoice_year):
        invoice = Invoice.objects.filter(
                                        credit_card=credit_card,
                                        month=invoice_month,
                                        year=invoice_year
                                    ).first()

        if invoice:
            if invoice.paid:
                invoice.paid = False
                invoice.save()
        else:
            invoice = Invoice.objects.create(
                                            credit_card=credit_card,
                                            month=invoice_month,
                                            year=invoice_year,
                                            amount_paid=0.00,
                                            paid=False
                                        )

        return invoice


    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction_type = self.cleaned_data.get("transaction_type")
        previous_transaction_type = self.instance.type if self.instance.pk else None
        
        if commit:
            transaction.save()
            
            # Se o tipo de transação mudou de 'card' para 'account' ou vice-versa
            if previous_transaction_type != transaction_type:
                # Se o tipo anterior era 'card' e mudou para 'account', excluir as CardTransactions
                if previous_transaction_type == "card":
                    CardTransaction.objects.filter(transaction=transaction).delete()
                else:
                    AccountTransaction.objects.filter(transaction=transaction).delete()
            
            
            if transaction_type == "card":
                credit_card = self.cleaned_data.get("credit_card")
                payment_at = self.cleaned_data.get("payment_at")
                num_installments = self.cleaned_data.get("installments")
                
                # Obter as transações existentes
                existing_card_transactions = CardTransaction.objects.filter(
                    transaction=transaction,
                    credit_card=credit_card
                )
                
                # Remover transações extras, se o número de parcelas diminuiu
                if len(existing_card_transactions) > num_installments:
                    extra_transactions = existing_card_transactions[num_installments:]
                    for extra_transaction in extra_transactions:
                        extra_transaction.delete()
                
                for i in range(0, num_installments):
                    last_day_of_month = calendar.monthrange(payment_at.year, payment_at.month)[1]
                    if payment_at.day == last_day_of_month:
                        invoice_month = (payment_at.month % 12) + 1
                        invoice_year = payment_at.year if payment_at.month != 12 else payment_at.year + 1
                        last_day_of_next_month = calendar.monthrange(invoice_year, invoice_month)[1]
                        payment_at = payment_at.replace(day=last_day_of_next_month, month=invoice_month, year=invoice_year)
                    else:
                        invoice_month = payment_at.month if payment_at.day <= credit_card.closing_day else (payment_at.month % 12) + 1
                        invoice_year = payment_at.year if payment_at.month == invoice_month or payment_at.month != 12 else payment_at.year + 1
                    
                    # Criar ou buscar a fatura para o cartão de crédito
                    invoice = self.get_or_create_invoice(credit_card, invoice_month, invoice_year)
                    
                    # Verificar se já existe uma CardTransaction para a parcela
                    card_transaction = existing_card_transactions.filter(
                        invoice=invoice,
                        installment_number=i + 1
                    ).first()
                    
                    if not card_transaction:
                        # Criar uma nova CardTransaction para cada parcela com o valor especificado
                        CardTransaction.objects.create(
                            transaction=transaction,
                            credit_card=credit_card,
                            invoice=invoice,
                            installment_number=i + 1,  # Número da parcela
                        )
                    else:
                        # Atualizar a transação existente
                        card_transaction.transaction = transaction
                        card_transaction.credit_card = credit_card
                        card_transaction.invoice = invoice
                        card_transaction.installment_number = i + 1
                        card_transaction.save()
                    
                    # Atualizar a data de pagamento para a próxima parcela
                    payment_at = payment_at.replace(month=(payment_at.month % 12) + 1, year=invoice_year)
            
            if transaction_type == 'account':
                # Verificar se já existe uma AccountTransaction para a transação
                account_transaction = AccountTransaction.objects.filter(
                    transaction=transaction
                ).first()
                
                if not account_transaction:
                    # Criar uma nova AccountTransaction
                    AccountTransaction.objects.create(
                        transaction=transaction,
                        account=self.cleaned_data.get("account"),
                        expire_at=self.cleaned_data.get("expire_at"),
                    )
                else:
                    account_transaction.transaction = transaction
                    account_transaction.account = self.cleaned_data.get("account")
                    account_transaction.expire_at = self.cleaned_data.get("expire_at")
                    account_transaction.save()
        
        return transaction


class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name', 'limit', 'additional_info', 'brand', 'closing_day', 'due_day']

    def clean(self):
        cleaned_data = super().clean()
        closing_day = cleaned_data.get('closing_day')
        due_day = cleaned_data.get('due_day')

        if closing_day and due_day:
            # Regra 1: Fechamento e vencimento não podem ser no mesmo dia
            if closing_day == due_day:
                raise forms.ValidationError("O dia de fechamento e o dia de vencimento não podem ser iguais.")

            # Regra 2: O vencimento deve ser após o fechamento OU nos primeiros dias do mês seguinte
            if not (due_day > closing_day or (closing_day >= 27 and due_day <= 10)):
                raise forms.ValidationError(
                    "O dia de vencimento deve ser posterior ao fechamento ou estar dentro dos primeiros 10 dias do mês seguinte."
                )

        return cleaned_data
    
class InvoicePaymentForm(forms.ModelForm):
    account = forms.ModelChoiceField(
        queryset=Account.objects.all(),
        required=True,
        label="Conta"
    )
    
    payment_at = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Data de Pagamento"
    )
    
    class Meta:
        model = Transaction
        fields = ['amount', 'attachment', 'account', 'payment_at']
        
    def clean(self):
        cleaned_data = super().clean()

        account = cleaned_data.get('account')
        payment_at = cleaned_data.get('payment_at')
            
        if not account:
            self.add_error('account', 'Informe a conta bancária')
            
        if not payment_at:
            self.add_error('payment_at', 'Informe a data de pagamento')
        
        return cleaned_data

    def save(self, commit=True, invoice=None, user=None):

        print("Caiu no save")

        if invoice is None:
            raise ValueError("O parâmetro 'invoice' não pode ser None")
    
        if user is None:
            raise ValueError("O parâmetro 'user' não pode ser None")
    
        transaction = super().save(commit=False)
    
        # Define o usuário da transação
        transaction.user = user
    
        # Definir a descrição padrão
        transaction.description = f"Pagamento de Fatura do Cartão {invoice.credit_card.name} - {invoice.month:02d}/{invoice.year}"
    
        # Verificar se a categoria "Faturas" existe, caso contrário, criar
        category, created = Category.objects.get_or_create(
            user=user,  # Usa o usuário logado
            name="Faturas",
            defaults={'color': '#000000', 'type': 'expense'}
        )
        transaction.category = category
    
        if commit:
            transaction.save()
        
            # Criar a AccountTransaction
            AccountTransaction.objects.create(
                transaction=transaction,
                account=self.cleaned_data.get("account"),
                expire_at=self.cleaned_data.get("payment_at"),  # expire_at igual a payment_at
            )
        
            # Atualizar o saldo da conta
            account = self.cleaned_data.get("account")
            account.balance -= transaction.amount
            account.save()
        
            # Atualizar o valor pago na fatura
            invoice.amount_paid += transaction.amount
            if invoice.balance_due == 0:
                invoice.paid = True
            invoice.save()
    
        return transaction