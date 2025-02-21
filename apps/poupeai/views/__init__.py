from .accounts import accounts_view
from .categories import categories_view
from .creditcard import creditcard_view
from .dashboard import dashboard_view
from .help import help_view
from .mygoals import mygoals_view
from .profile import profile_view
from .transactions import transactions_view
from .account_deletion import account_deletion_view
from .admin_dashboard import admin_view
from .notifications import *

__all__ = [
    'accounts_view',
    'categories_view',
    'creditcard_view',
    'dashboard_view',
    'help_view',
    'mygoals_view',
    'profile_view',
    'transactions_view',
    'account_deletion_view',
    'admin_view',
    'notifications_view',
]