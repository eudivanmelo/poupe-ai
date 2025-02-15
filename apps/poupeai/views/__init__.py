from .finance.accounts import accounts_view
from .finance.categories import CategoriesView
from .finance.credit_cards import creditcard_view
from .core.dashboard import dashboard_view
from .core.help import help_view
from .finance.goals import mygoals_view
from .profile.profiles import profile_view
from .finance.transactions import transactions_view
from .profile.profiles import profile_deletion_view
from .admin_dashboard import admin_view
from .core.home import home_view
from .core.notifications import notifications_view

__all__ = [
    'home_view',
    'accounts_view',
    'CategoriesView',
    'creditcard_view',
    'dashboard_view',
    'help_view',
    'mygoals_view',
    'profile_view',
    'transactions_view',
    'profile_deletion_view',
    'admin_view',
    'notifications_view',
]