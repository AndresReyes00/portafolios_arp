from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = 'my_apps.accounts'


    def ready(self):
        import my_apps.accounts.signals