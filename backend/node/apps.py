from django.apps import AppConfig
import asyncio
import websockets
import json
from django.apps import AppConfig
import threading
class NodeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "node"
    whoim=""
    
    def ready(self):
        from .node_websocket_client import start_client
        threading.Thread(target=start_client, daemon=True).start()
