from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.poupeai'

    def ready(self):
        import apps.poupeai.signals