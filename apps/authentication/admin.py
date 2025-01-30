from django.contrib import admin
from apps.authentication.models import CustomUser, PasswordRecovery

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_superuser', 'create_at', 'update_at']
    search_fields = ['email', 'name', 'phone']
    ordering = ['email', 'name', 'create_at', 'update_at']
    
class PasswordRecoveryAdmin(admin.ModelAdmin):
    model = PasswordRecovery
    list_display = ['id_user', 'token', 'create_at', 'expiration_date']
    search_fields = ['id_user', 'token']
    ordering = ['id_user', 'create_at', 'expiration_date']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PasswordRecovery, PasswordRecoveryAdmin)