from django.contrib import admin
from apps.poupeai.models import Account, Goal, Category, Transaction, CreditCard, CardTransaction, Invoice, AccountTransaction, GoalDeposit

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'balance', 'created_at']
    search_fields = ['user__email', 'name']
    ordering = ['user', 'name', 'created_at']

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'goal', 'status', 'created_at']
    search_fields = ['user__email', 'name']
    ordering = ['user', 'name', 'created_at']

@admin.register(GoalDeposit)
class GoalDepositAdmin(admin.ModelAdmin):
    list_display = ['goal__name', 'deposit_amount', 'deposit_at']
    search_fields = ['goal__name', 'deposit_at']
    ordering = ['goal', 'deposit_at']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'type', 'created_at', 'updated_at']
    search_fields = ['name']
    ordering = ['name', 'created_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'description', 'amount', 'category', 'created_at', 'payment_at']
    search_fields = ['user__email', 'description']
    ordering = ['user', 'description', 'created_at']

@admin.register(CreditCard)
class CreditCardAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'brand', 'limit', 'closing_day', 'due_day', 'outstanding', 'available', 'created_at']
    search_fields = ['user__name', 'user__email', 'name', 'brand']
    ordering = ['user', 'name', 'limit']

@admin.register(CardTransaction)
class CardTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'credit_card', 'invoice')
    search_fields = ('transaction__description', 'credit_card__name', 'invoice__month')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('credit_card', 'month', 'year', 'total_due', 'amount_paid', 'balance_due', 'paid', 'status')
    list_filter = ('month', 'year')
    search_fields = ('credit_card__name',)

@admin.register(AccountTransaction)
class AccountTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'account', 'expire_at')
    search_fields = ('transaction__description', 'credit_card__name', 'invoice__month')