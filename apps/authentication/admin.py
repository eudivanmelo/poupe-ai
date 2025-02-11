from django.contrib import admin
from apps.authentication.models import CustomUser, PasswordRecovery

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_superuser', 'create_at', 'update_at']
    search_fields = ['email', 'name', 'phone']
    ordering = ['email', 'name', 'create_at', 'update_at']
    
@admin.register(PasswordRecovery)
class PasswordRecoveryAdmin(admin.ModelAdmin):
    model = PasswordRecovery
    list_display = ['id_user', 'token', 'create_at', 'expire_at']
    search_fields = ['id_user', 'token']
    ordering = ['id_user', 'create_at', 'expire_at']