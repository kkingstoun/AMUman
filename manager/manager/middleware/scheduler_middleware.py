# myapp/middleware.py

import os
import logging

from django.core.exceptions import MiddlewareNotUsed

from manager.components.scheduler import ThreadedScheduler
from manager.components.queueManager import QueueManager

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
        log = logging.getLogger("rich")
        #log.debug("reqqq", request)
        #log.debug("Starting job scheduling...")
        try:
            # Avoid starting multiple schedulers
           
            #log.debug(self.scheduler.get_jobs())
            if not self.scheduler.get_jobs():
                #log.debug("if not!!")
                log.debug("Starting job scheduling...")
                self.scheduler.every(10).seconds.do(QueueManager().prepare_job)
                self.scheduler.start()
            else:
                pass
        except Exception as e:
            log.debug(f"Error starting scheduler: {e}")


        return response
