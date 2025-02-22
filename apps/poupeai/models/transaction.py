from django.db import models
from django.db.models import Sum
from apps.authentication.models import CustomUser
from .account import Account
from .category import Category
from .credit_card import CreditCard, Invoice
from datetime import date

TRANSACTION_TYPES = (
    ('income', 'Receita'),
    ('expense', 'Despesa'),
)

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")
    
    payment_at = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def type(self):
        if hasattr(self, 'account_transaction'):
            return self.category.type
        elif hasattr(self, 'card_transactions'):
            return 'card'
        return 'Desconhecido'

    @property
    def status(self):
        if hasattr(self, 'account_transaction'):
            expire_at = self.account_transaction.expire_at
            payment_at = self.payment_at
            today = date.today()
            
            if payment_at:
                return 'paid'
            
            if expire_at < today:
                return 'expired'
            
            if 0 <= (expire_at - today).days < 10:
                return 'warning'
            
            return 'unpaid'
        
        if hasattr(self, 'card_transactions'):
            return 'paid'

        return 'paid'
    
    @property
    def installments_total_amount(self):
        return self.card_transactions.aggregate(Sum('transaction__amount'))['transaction__amount__sum'] or 0
    
    @property
    def total_installments(self):
        if hasattr(self, 'card_transactions'):
            return self.card_transactions.count()
        
    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return self.description

class CardTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="card_transactions")
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="credit_card")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name="card_transactions")
    
    installment_number = models.PositiveSmallIntegerField(default=1)
    
    class Meta:
        verbose_name = "Transação de Cartão"
        verbose_name_plural = "Transações de Cartão"

    def __str__(self):
        return self.transaction.description

class AccountTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="account_transaction")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_transactions")

    expire_at = models.DateField()

    class Meta:
        verbose_name = "Transação de Conta"
        verbose_name_plural = "Transações de Conta"

    def __str__(self):
        return self.transaction.description