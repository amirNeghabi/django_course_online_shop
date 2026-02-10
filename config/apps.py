from django.apps import AppConfig


class ConfigConfig(AppConfig):
    name = 'config'
    
    def ready(self):
        # Import admin configuration to apply customizations
        from . import admin
