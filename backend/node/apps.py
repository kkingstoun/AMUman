from django.apps import AppConfig
import asyncio
import websockets
import json

from django.apps import AppConfig
from .node_websocket_client import start_client
import threading
class NodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "node"
    whoim=""
    
    def ready(self):
        threading.Thread(target=start_client, daemon=True).start()


    # def ready(self):
    #     self.gpm = GPUMonitor()

