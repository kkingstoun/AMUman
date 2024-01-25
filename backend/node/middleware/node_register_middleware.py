# app_name/middleware.py

from django.conf import settings
from ..management.commands.runnode import Command as RunNodeCommand
from django.core.exceptions import MiddlewareNotUsed
import requests

class NodeStartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.run_once = False
        # if not settings.DEBUG:  # Opcjonalnie: uruchom tylko w środowisku produkcyjnym
        self.run_node_startup()
        raise MiddlewareNotUsed("NodeStartupMiddleware is only used once.")

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def run_node_startup(self):
        # Logika zgłoszenia do mastera
        run_node_command = RunNodeCommand()
        run_node_command.handle()
        
    
