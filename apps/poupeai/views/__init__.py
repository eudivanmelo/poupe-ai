from .admin_dashboard import admin_view

from .core.dashboard import dashboard_view, relatory_view
from .core.help import HelpView
from .core.home import home_view
from .core.notifications import notifications_view

from .finance.accounts import AccountsListView, AccountCreateView, AccountDeleteView, AccountDetailView, AccountUpdateView

from .finance.categories import CategoriesListView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView

from .finance.credit_cards import CreditCardsView

from .finance.goals import GoalsListView, GoalCreateView, GoalDeleteView, GoalUpdateView, GoalDepositCreateView

from .finance.transactions import TransactionsListView, TransactionDeleteView, TransactionDetailView, TransactionCreateView, TransactionUpdateView

from .profile.profiles import ProfileDeleteView
from .profile.profiles import ProfileView


__all__ = [
    'admin_view',
    'dashboard_view',
    'relatory_view',

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
    
    'CreditCardsView',
    
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