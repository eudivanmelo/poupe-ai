from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('ai/relatory/', relatory_view, name='ai-relatory'),
    path('ai/tip/', tip_view, name='ai-tip'),
    path('chart/category/', category_chart_data, name='category-chart'),
    path('chart/cards/', cards_analytics_chart_data, name='cards-chart'),
    path('chart/balance/', balance_analytics_chart_data, name='balance-chart'),
    
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category-update'),
    
    path('transactions/', TransactionsListView.as_view(), name='transactions'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction-create'),
    path('transaction/delete/<int:pk>/', TransactionDeleteView.as_view(), name='transaction-delete'),
    path('transaction/update/<int:pk>/', TransactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/detail/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('account/create/', AccountCreateView.as_view(), name='account-create'),
    path('account/delete/<int:pk>/', AccountDeleteView.as_view(), name='account-delete'),
    path('account/detail/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('account/update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
  
    path('credit-cards/', CreditCardsListView.as_view(), name='credit-cards'),
    path('credit-card/create/', CreditCardCreateView.as_view(), name='credit-card-create'),
    path('credit-card/delete/<int:pk>/', CreditCardDeleteView.as_view(), name='credit-card-delete'),
    path('credit-card/update/<int:pk>/', CreditCardUpdateView.as_view(), name='credit-card-update'),
    path('credit-card/payment/<int:pk>/', InvoicePaymentView.as_view(), name='credit-card-payment'),

    path('goals/', GoalsListView.as_view(), name='goals'),
    path('goal/create/', GoalCreateView.as_view(), name='goal-create'),
    path('goal/delete/<int:pk>/', GoalDeleteView.as_view(), name='goal-delete'),
    path('goal/update/<int:pk>/', GoalUpdateView.as_view(), name='goal-update'),
    path('goal/deposit/<int:pk>/', GoalDepositCreateView.as_view(), name='goal-deposit'),
    
    path('help/', HelpView.as_view(), name='help'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/delete/', ProfileDeleteView.as_view(), name='profile-delete'),

    path('user/admin/', admin_view, name='admin-dashboard'),
]