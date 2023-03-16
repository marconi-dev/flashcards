from django.apps import AppConfig


class BaralhosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baralhos'
  
    def ready(self):
        import baralhos.signals