# myapp/middleware.py

import os

from django.core.exceptions import MiddlewareNotUsed

from manager.components.scheduler import ThreadedScheduler


class SchedulerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        if not (
            os.environ.get("RUN_MAIN")
            or "runserver" in os.environ.get("DJANGO_SETTINGS_MODULE", "")
        ):
            raise MiddlewareNotUsed()
        self.scheduler = ThreadedScheduler.get_instance()

    def __call__(self, request):
        response = self.get_response(request)
        return response
