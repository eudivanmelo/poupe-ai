from django.db import models

TRANSACTION_TYPES = (
    ('income', 'Receita'),
    ('expense', 'Despesa'),
)

class Category(models.Model):
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
