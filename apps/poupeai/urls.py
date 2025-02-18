from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('transactions/', transactions_view, name='transactions'),
    
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('account/create/', AccountCreateView.as_view(), name='account-create'),
    path('account/delete/<int:pk>/', AccountDeleteView.as_view(), name='account-delete'),
    path('account/detail/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('account/update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
    
    path('credit-card/', creditcard_view, name='credit-card'),
    path('my-goals/', mygoals_view, name='my-goals'),
    path('help/', help_view, name='help'),
    path('profile/', profile_view, name='profile'),
    path('profile/deletion/', profile_deletion_view, name='profile-deletion'),
    path('user/admin/', admin_view, name='admin-dashboard'),
    path('notifications/', notifications_view, name='notifications'),
]