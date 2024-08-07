import logging

from constance.signals import config_updated
from django.dispatch import receiver

from manager.components.scheduler import ThreadedScheduler

from .components.queueManager import QueueManager

log = logging.getLogger("rich")


# @receiver(config_updated)
# def constance_updated(sender, key, old_value, new_value, **kwargs):
#     scheduler = ThreadedScheduler.get_instance()
#     if key == "autorun_jobs" and new_value is True and not old_value:
#         try:
#             # Avoid starting multiple schedulers
#             if not scheduler.get_jobs():
#                 scheduler.every(1).seconds.do(QueueManager().schedule_jobs)
#                 scheduler.start()
#             else:
#                 scheduler.start()
#         except Exception as e:
#             log.debug(f"Error starting scheduler: {e}")
#     else:
#         try:
#             scheduler.stop()
#         except Exception as e:
#             log.debug(f"Error stopping scheduler: {e}")
