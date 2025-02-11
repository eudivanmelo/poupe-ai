from django.db import models
from apps.authentication.models import CustomUser

class Goal(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="goals")

    name = models.CharField(max_length=255)
    motivation = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7)
    priority = models.IntegerField(default=0)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    target_at = models.DateField()
    completed_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        
    @property
    def status(self):
        if self.completed_at:
            return 'Concluído'
        return 'Em andamento'

    def __str__(self):
        return self.name

class GoalDeposit(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="deposits")

    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_at = models.DateField()
    note = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Depósito da Meta"
        verbose_name_plural = "Depósitos das Metas"

    def __str__(self):
        return f"Depósito de {self.deposit_amount} em {self.deposit_at}"
