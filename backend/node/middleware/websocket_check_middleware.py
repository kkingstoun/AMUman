import os
from django.core.exceptions import MiddlewareNotUsed
import threading
import time
class WebSocketMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not (os.environ.get('RUN_MAIN') or 'runserver' in os.environ.get('DJANGO_SETTINGS_MODULE', '')):
            raise MiddlewareNotUsed()
        
        self.run_websocket_startup()
        
    def __call__(self, request):
        response = self.get_response(request)
        if "websocket" in request.META.get('UPGRADE', '').lower():
            print("WebSocket connection attempt.")
        return response 
    
    def run_websocket_startup(self):
        from node.node_websocket_client import start_client
        threading.Thread(target=start_client, daemon=True).start()
