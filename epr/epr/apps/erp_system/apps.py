from django.apps import AppConfig


class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'erp_system'
    #
    # def ready(self):
    #     import erp_system.signal
