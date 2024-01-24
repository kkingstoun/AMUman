from django.apps import AppConfig

class NodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "node"
    
    # def ready(self):
    #     self.gpm = GPUMonitor()