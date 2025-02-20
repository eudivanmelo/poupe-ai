from django.db import models
from apps.authentication.models import CustomUser
from django.db.models import Sum

TRANSACTION_TYPES = (
    ('income', 'Receita'),
    ('expense', 'Despesa'),
)

class Category(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name
    
    @property
    def total_transactions_value(self):
        """Returns the total value of transactions associated with this category."""
        total = self.transactions.aggregate(total=Sum('amount'))['total']
        return total or 0
