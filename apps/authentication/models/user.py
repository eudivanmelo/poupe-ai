from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from apps.authentication.managers import CustomUserManager

class PasswordRecovery(models.Model):
    id_user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name="password_recoveries")
    token = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        verbose_name = 'Recuperação de Senha'
        verbose_name_plural = 'Recuperações de Senha'

    def __str__(self):
        return f'{self.id_user.email} - {self.token}'


class CustomUser(AbstractBaseUser, PermissionsMixin):
    SEX_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
    )

    email = models.EmailField(unique=True)
    
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    last_login = models.DateTimeField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email