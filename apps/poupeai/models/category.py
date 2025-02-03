from django.db import models

transactions_type = (
    ('income', 'Receita'),
    ('expense', 'Despesa'),
)

class Category(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)
    type = models.CharField(max_length=7, choices=transactions_type)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    