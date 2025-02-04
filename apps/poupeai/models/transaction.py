from django.db import models
from apps.authentication.models import CustomUser
from apps.poupeai.models import Category
from apps.poupeai.models.creditcard import CreditCard, Invoice

class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    description = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    fixed = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)
    transaction_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description

class CardTransaction(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f'Transação {self.transaction.description} com {self.credit_card.name}'