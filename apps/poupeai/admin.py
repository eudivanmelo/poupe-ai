from django.contrib import admin
from apps.poupeai.models import Account, Goal, Category, Transaction, Brand, CreditCard, CardTransaction, Invoice

class AccountAdmin(admin.ModelAdmin):
    model = Account
    list_display = ['user', 'name', 'balance', 'created_at']
    search_fields = ['user', 'name']
    ordering = ['user', 'name', 'created_at']

admin.site.register(Account, AccountAdmin)
    
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
    
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ['user', 'description', 'value', 'category', 'transaction_date', 'created_at']
    search_fields = ['user', 'description']
    ordering = ['user', 'description', 'created_at']

class BrandAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

class CreditCardAdmin(admin.ModelAdmin):
    model = CreditCard
    list_display = ['user', 'name', 'brand', 'limit', 'closing_day', 'due_day', 'created_at']
    search_fields = ['user__name', 'user__email', 'name', 'brand__name']
    ordering = ['user', 'name', 'limit']

class CardTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'credit_card', 'invoice')
    search_fields = ('transaction__description', 'credit_card__name', 'invoice__month')

admin.site.register(CardTransaction, CardTransactionAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('credit_card', 'month', 'year', 'total_amount', 'paid_amount', 'remaining_balance', 'paid')
    list_filter = ('paid', 'month', 'year')
    search_fields = ('credit_card__name',)

admin.site.register(Invoice, InvoiceAdmin)

admin.site.register(Goal, GoalAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(CreditCard, CreditCardAdmin)