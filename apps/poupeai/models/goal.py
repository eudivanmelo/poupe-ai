from django.db import models

class Goal(models.Model):
    name = models.CharField(max_length=255)
    motivation = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=7)
    priority = models.IntegerField()
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, default='A')
    target_date = models.DateField()
    completed_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name