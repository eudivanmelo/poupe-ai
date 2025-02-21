from django import forms
from .models import Transaction, CardTransaction, AccountTransaction
from .models import CreditCard, Account, Invoice

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
        
        if transaction_type == 'card':
            credit_card = cleaned_data.get('credit_card')
            payment_at = cleaned_data.get('payment_at')
            
            if not credit_card:
                self.add_error('credit_card', 'Este campo é obrigatório')
                
            if not payment_at:
                self.add_error('payment_at', 'Este campo é obrigatório')
        
        if transaction_type == 'account':
            account = cleaned_data.get('account')
            expire_at = cleaned_data.get('expire_at')
            
            if not account:
                self.add_error('account', 'Este campo é obrigatório')
            
            if not expire_at:
                self.add_error('expire_at', 'Este campo é obrigatório')
        
        return cleaned_data
    
    def get_or_create_invoice(self, credit_card, invoice_month, invoice_year):
        invoice = Invoice.objects.filter(
                                        credit_card=credit_card,
                                        month=invoice_month,
                                        year=invoice_year
                                    ).first()

        if not invoice:
            invoice = Invoice.objects.create(
                                            credit_card=credit_card,
                                            month=invoice_month,
                                            year=invoice_year,
                                            total_due=0.00,
                                            amount_paid=0.00,
                                            balance_due=0.00,
                                            paid=False
                                        )

        return invoice


    
    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction_type = self.cleaned_data.get("transaction_type")
        
        if commit:
            transaction.save()
            
            if transaction_type == "card":
                credit_card = self.cleaned_data.get("credit_card")
                payment_at = self.cleaned_data.get("payment_at")
                
                for i in range(0, self.cleaned_data.get("installments")):
                    invoice_month = payment_at.month if payment_at.day <= credit_card.closing_day else (payment_at.month % 12) + 1
                    invoice_year = payment_at.year if payment_at.month == invoice_month else payment_at.year + 1
                    
                    # Criar ou buscar a fatura para o cartão de crédito
                    invoice = self.get_or_create_invoice(credit_card, invoice_month, invoice_year)
                    
                    # Criar uma nova CardTransaction para cada parcela com o valor especificado
                    CardTransaction.objects.create(
                        transaction=transaction,
                        credit_card=credit_card,
                        invoice=invoice,
                        installment_number=i + 1,  # Número da parcela
                    )
                    
                    # Atualizar a data de pagamento para a próxima parcela
                    payment_at = payment_at.replace(month=(payment_at.month % 12) + 1)
                
            if transaction_type == 'account':
                AccountTransaction.objects.create(
                    transaction=transaction,
                    account=self.cleaned_data.get("account"),
                    expire_at=self.cleaned_data.get("expire_at"),
                )
        
        return transaction
