from django.db import models
from apps.authentication.models import CustomUser
from .account import Account
from .category import Category
from .creditcard import CreditCard, Invoice

TRANSACTION_TYPES = (
    ('income', 'Receita'),
    ('expense', 'Despesa'),
)

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="transactions")

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fixed = models.BooleanField(default=False)
    attachment = models.FileField(upload_to="attachments/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transação"
        verbose_name_plural = "Transações"

    def __str__(self):
        return self.description

class CardTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="card_transaction")
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="card_transactions")
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name="card_transactions")

    class Meta:
        verbose_name = "Transação de Cartão"
        verbose_name_plural = "Transações de Cartão"

    def __str__(self):
        return self.transaction.description

class AccountTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name="account_transaction")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="account_transactions")

    expire_at = models.DateField()
    payment_at = models.DateField()
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)

    class Meta:
        verbose_name = "Transação de Conta"
        verbose_name_plural = "Transações de Conta"

    def __str__(self):
        return self.transaction.description