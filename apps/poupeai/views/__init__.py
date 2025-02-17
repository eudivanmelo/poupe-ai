from .admin_dashboard import admin_view

from .core.dashboard import dashboard_view
from .core.help import help_view
from .core.home import home_view
from .core.notifications import notifications_view

from .finance.accounts import accounts_view
from .finance.categories import CategoriesView
from .finance.credit_cards import creditcard_view
from .finance.goals import mygoals_view
from .finance.transactions import transactions_view

from .profile.profiles import profile_deletion_view
from .profile.profiles import profile_view

__all__ = [
    'admin_view',
    'dashboard_view',
    'help_view',
    'home_view',
    'notifications_view',
    'accounts_view',
    'CategoriesView',
    'creditcard_view',
    'mygoals_view',
    'transactions_view',
    'profile_deletion_view',
    'profile_view',
]