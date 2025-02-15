from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('transactions/', transactions_view, name='transactions'),
    path('accounts/', accounts_view, name='accounts'),
    path('credit-cards/', creditcard_view, name='credit-cards'),
    path('goals/', mygoals_view, name='goals'),
    path('help/', help_view, name='help'),
    path('profile/', profile_view, name='profile'),
    path('profile/deletion/', profile_deletion_view, name='profile-deletion'),
    path('user/admin/', admin_view, name='admin-dashboard'),
    path('notifications/', notifications_view, name='notifications'),
]