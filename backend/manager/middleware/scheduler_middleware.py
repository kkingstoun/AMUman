# myapp/middleware.py

from django.core.exceptions import MiddlewareNotUsed
from manager.components.scheduler import ThreadedScheduler
import os

class SchedulerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Sprawdzamy, czy uruchamiamy w kontekście serwera developerskiego
        if not (os.environ.get('RUN_MAIN') or 'runserver' in os.environ.get('DJANGO_SETTINGS_MODULE', '')):
            raise MiddlewareNotUsed()
        # Inicjalizacja schedulera
        self.scheduler = ThreadedScheduler.get_instance()
        
    def __call__(self, request):
        # Przekazujemy żądanie dalej w łańcuchu middleware
        response = self.get_response(request)
        return response
