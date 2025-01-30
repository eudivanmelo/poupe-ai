from django.contrib import admin
from apps.poupeai.models import Account

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ['user', 'name', 'balance', 'created_at']
    search_fields = ['user', 'name']
    ordering = ['user', 'name', 'created_at']
    
admin.site.register(Account, AccountAdmin)

