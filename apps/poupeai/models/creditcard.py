from django.db import models
from django.forms import ValidationError
from apps.authentication.models import CustomUser

def validate_day(value):
    """Garante que o dia esteja entre 1 e 31."""
    if not (1 <= value <= 31):
        raise ValidationError("O dia deve estar entre 1 e 31.")

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Bandeira"
        verbose_name_plural = "Bandeiras"

class CreditCard(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=255)
    limit = models.DecimalField(max_digits=10, decimal_places=2)
    additional_details = models.TextField(blank=True, null=True)
    closing_day = models.PositiveSmallIntegerField(validators=[validate_day])
    due_day = models.PositiveSmallIntegerField(validators=[validate_day])

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

    class Meta:
        verbose_name = "Cartão de Crédito"
        verbose_name_plural = "Cartões de Crédito"