from django.contrib import admin
from apps.poupeai.models import Account, Goal, Category

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ['user', 'name', 'balance', 'created_at']
    search_fields = ['user', 'name']
    ordering = ['user', 'name', 'created_at']
    
class GoalAdmin(admin.ModelAdmin):
    model = Goal
    list_display = ['user', 'name', 'goal', 'status', 'created_at']
    search_fields = ['user', 'name']
    ordering = ['user', 'name', 'created_at']
    
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'color', 'type', 'created_at']
    search_fields = ['name']
    ordering = ['name', 'created_at']
    
admin.site.register(Account, AccountAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(Category, CategoryAdmin)

