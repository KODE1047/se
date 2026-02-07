# circulation/apps.py
from django.apps import AppConfig

class CirculationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'circulation'
    
    def ready(self):
        # Import signals here if we add them later for status updates
        pass