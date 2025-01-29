from django.contrib import admin
from apps.authentication.models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_superuser', 'create_at', 'update_at']
    search_fields = ['email', 'name', 'phone']
    ordering = ['email', 'name', 'create_at', 'update_at']

admin.site.register(CustomUser, CustomUserAdmin)