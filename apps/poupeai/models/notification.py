from django.db import models
from apps.authentication.models import CustomUser


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="Notificações")

    title = models.CharField(max_length=255)
    mensage = models.TextField()
    creat_date = models.DateTimeField(auto_now_add=True)

    read = 'Lida'
    not_read = 'Não lida'

    status_choice = [
        (read, 'lida' ),
        (not_read, 'Não lida'),
    ]

    status = models.models.CharField(max_length=10, choices=status_choice, default=not_read)
    seen = models.BooleanField(default=False)

    pass