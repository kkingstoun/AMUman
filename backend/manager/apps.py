from django.apps import AppConfig
from manager.scheduler import start_scheduler
class MasterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "manager"
