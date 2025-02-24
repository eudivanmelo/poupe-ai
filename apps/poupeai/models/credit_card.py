from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from apps.authentication.models import CustomUser
from decimal import Decimal
from datetime import date
import calendar

def validate_day(value):
    """Garante que o dia esteja entre 1 e 31."""
    if not (1 <= value <= 31):
        raise ValidationError("O dia deve estar entre 1 e 31.")

class CreditCard(models.Model):
    class BrandChoices(models.TextChoices):
        VISA = "VISA", "Visa"
        MASTERCARD = "MASTERCARD", "Mastercard"
        AMEX = "AMEX", "American Express"
        ELO = "ELO", "Elo"
        HIPERCARD = "HIPERCARD", "Hipercard"

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="credit_cards")
    brand = models.CharField(max_length=20, choices=BrandChoices.choices, null=True, blank=True)

    name = models.CharField(max_length=255)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    additional_info = models.TextField(blank=True, null=True)
    closing_day = models.PositiveSmallIntegerField(validators=[validate_day])
    due_day = models.PositiveSmallIntegerField(validators=[validate_day])

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cartão de Crédito"
        verbose_name_plural = "Cartões de Crédito"

    def __str__(self):
        return f"{self.user.email} - {self.name}"
    
    @property   
    def outstanding(self):
        total = sum(invoice.total_due for invoice in self.invoices.filter(paid=False))
        return Decimal(total or 0)

    @property
    def available(self):
        return self.limit - self.outstanding

class Invoice(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="invoices")

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"

    def __str__(self):
        status = "Paga" if self.paid else "Pendente"
        return f"Fatura {self.month}/{self.year} - R$ {self.total_due:.2f} ({status})"
    
    @property
    def total_due(self):
        total = self.card_transactions.filter(invoice=self).aggregate(total=Sum('transaction__amount'))['total']
        return Decimal(total or 0)
    
    @property
    def balance_due(self):
        return self.total_due - self.amount_paid
    
    @property
    def status(self):
        today = date.today()
    
        _, num_days_in_month = calendar.monthrange(self.year, self.month)
    
        closing_day = min(self.credit_card.closing_day, num_days_in_month)
    
        closing_date = date(self.year, self.month, closing_day)
    
        if today > closing_date:
            return 'closed'
        else:
            return 'open'