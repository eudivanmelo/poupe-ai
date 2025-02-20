from django.db import models
from django.core.exceptions import ValidationError
from apps.authentication.models import CustomUser

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

class Invoice(models.Model):
    credit_card = models.ForeignKey(CreditCard, on_delete=models.CASCADE, related_name="invoices")

    month = models.PositiveSmallIntegerField()
    year = models.PositiveSmallIntegerField()
    total_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Fatura"
        verbose_name_plural = "Faturas"

    def __str__(self):
        status = "Paga" if self.paid else "Pendente"
        return f"Fatura {self.month}/{self.year} - R$ {self.total_due:.2f} ({status})"