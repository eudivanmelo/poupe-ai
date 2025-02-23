from .admin_dashboard import admin_view

from .core.dashboard import DashboardView, relatory_view, tip_view
from .core.help import HelpView
from .core.home import home_view
from .core.notifications import notifications_view

from .finance.accounts import AccountsListView, AccountCreateView, AccountDeleteView, AccountDetailView, AccountUpdateView

from .finance.categories import CategoriesListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView
from .finance.credit_cards import CreditCardsListView, CreditCardCreateView, CreditCardDeleteView, CreditCardUpdateView, InvoicePaymentView

from .finance.goals import GoalsListView, GoalCreateView, GoalDeleteView, GoalUpdateView, GoalDepositCreateView

from .finance.transactions import TransactionsListView, TransactionDeleteView, TransactionDetailView, TransactionCreateView, TransactionUpdateView

from .profile.profiles import ProfileDeleteView
from .profile.profiles import ProfileView


__all__ = [
    'admin_view',
    'DashboardView',
    'relatory_view',
    'tip_view',

    'HelpView',
    
    'home_view',
    'notifications_view',
    
    'AccountsListView',
    'AccountCreateView',
    'AccountDeleteView',
    'AccountDetailView',
    'AccountUpdateView',
    
    'CategoriesListView',
    'CategoryCreateView',
    'CategoryDeleteView',
    'CategoryUpdateView',
    
    'CreditCardsListView',
    'CreditCardCreateView',
    'CreditCardDeleteView',
    'CreditCardUpdateView',
    'InvoicePaymentView',
    
    'GoalsListView',
    'GoalCreateView',
    'GoalDeleteView',
    'GoalUpdateView',
    'GoalDepositCreateView',
    
    'TransactionsListView',
    'TransactionDeleteView',
    'TransactionDetailView',
    'TransactionCreateView',
    'TransactionUpdateView',
    
    'ProfileDeleteView',
    'ProfileView',
]