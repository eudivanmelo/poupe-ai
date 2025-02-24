from django.db import models
from django.db.models import Sum
from apps.authentication.models import CustomUser

class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"

    def __str__(self):
        return f'{self.user.email} - {self.name}'
    
    @property
    def current_balance(self):
        """Retorna o saldo atual da conta."""
        total = self.balance + self.total_income - self.total_expense
        return total or 0
    
    @property
    def total_income(self):
        """Retorna o valor total das receitas (entradas) associadas a esta conta."""
        total = self.account_transactions.filter(transaction__category__type='income').aggregate(total=Sum('transaction__amount'))['total']
        return total or 0

    @property
    def total_expense(self):
        """Retorna o valor total das despesas (saídas) associadas a esta conta."""
        total = self.account_transactions.filter(transaction__category__type='expense') \
                                        .aggregate(total=Sum('transaction__amount'))['total']
        return total or 0