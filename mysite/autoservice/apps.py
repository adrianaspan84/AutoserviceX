from django.apps import AppConfig

class AutoserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservice'

    def ready(self):
        import autoservice.signals
