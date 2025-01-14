from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('categories/', categories_view, name='categories'),
    path('transactions/', transactions_view, name='transactions'),
    path('accounts/', accounts_view, name='accounts'),
    path('credit-card/', creditcard_view, name='credit-card'),
    path('my-goals/', mygoals_view, name='my-goals'),
    path('help/', help_view, name='help'),
    path('profile/', profile_view, name='profile'),
    path('account/deletion/', account_deletion_view, name='account-deletion'),
    path('user/admin/', admin_view, name='admin-dashboard'),
]