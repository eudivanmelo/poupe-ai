from django.db import models
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