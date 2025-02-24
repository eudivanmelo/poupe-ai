from django.db import models
from apps.authentication.models import CustomUser
from datetime import date

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
    def time_left(self):
        if self.completed_at:
            return "Concluido"
        
        today = date.today()
        delta_time = self.target_at - today
        
        if delta_time.days < 0:  # Caso a meta tenha sido excedida
            days_exceeded = abs(delta_time.days)
            if days_exceeded < 30:
                return f"Meta excedida há {days_exceeded} dias"
            months_exceeded = (today.year - self.target_at.year) * 12 + today.month - self.target_at.month
            return f"Meta excedida há {months_exceeded} meses"

        if delta_time.days < 30:
            return f"faltam {delta_time.days} dias"
        
        months = (self.target_at.year - self.created_at.year) * 12 + self.target_at.month - self.created_at.month
        return f"faltam {months} meses"    
    
    @property
    def current_balance(self):
        """ Retorna o saldo atual somando os depósitos ao saldo inicial. """
        return self.initial_balance + sum(deposit.deposit_amount for deposit in self.deposits.all())
    
    @property
    def amount_needed(self):
        """ Retorna o valor que falta para atingir a meta. """
        return self.goal - self.current_balance

    @property
    def monthly_amount_needed(self):
        """ Calcula quanto precisa ser depositado por mês para atingir a meta, mesmo se o prazo já passou. """
        if self.completed_at:
            return 0.0  # Já atingiu ou ultrapassou o valor da meta

        today = date.today()
        months_remaining = (self.target_at.year - today.year) * 12 + self.target_at.month - today.month
        amount_needed = self.goal - self.current_balance

        if amount_needed <= 0:
            return 0.0  # Já atingiu ou ultrapassou o valor da meta

        if months_remaining <= 0:
            months_elapsed = (today.year - self.created_at.year) * 12 + today.month - self.created_at.month
            return round(amount_needed / months_elapsed, 2) if months_elapsed > 0 else amount_needed

        return round(amount_needed / months_remaining, 2)
      
    @property
    def status(self):
        if self.completed_at:
            return 'done'
        return 'active'

    def __str__(self):
        return self.name

class GoalDeposit(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="deposits")

    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_at = models.DateField()
    note = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Depósito da Meta"
        verbose_name_plural = "Depósitos das Metas"

    def __str__(self):
        return f"Depósito de {self.deposit_amount} em {self.deposit_at}"
