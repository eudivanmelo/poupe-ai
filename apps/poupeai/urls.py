from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('transactions/', TransactionsView.as_view(), name='transactions'),
    
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('account/create/', AccountCreateView.as_view(), name='account-create'),
    path('account/delete/<int:pk>/', AccountDeleteView.as_view(), name='account-delete'),
    path('account/detail/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    path('account/update/<int:pk>/', AccountUpdateView.as_view(), name='account-update'),
  
    path('credit-cards/', CreditCardsView.as_view(), name='credit-cards'),
    path('goals/', GoalsView.as_view(), name='goals'),
    path('help/', help_view, name='help'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/deletion/', ProfileDeletionView.as_view(), name='profile-deletion'),
    path('user/admin/', admin_view, name='admin-dashboard'),
    path('notifications/', notifications_view, name='notifications'),
    path('profile/update-photo/', UpdateProfilePictureView.as_view(), name='update-profile-picture'),
]