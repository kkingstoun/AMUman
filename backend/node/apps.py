from django.apps import AppConfig



class NodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "node"
    whoim=""
    
    def ready(self):
        pass
