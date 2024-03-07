from django.db.models.signals import post_save
from django.dispatch import receiver

from manager.components.scheduler import ThreadedScheduler

from .components.queue import QueueManager
from .models import ManagerSettings


@receiver(post_save, sender=ManagerSettings)
def manage_scheduler_on_change(sender, instance, **kwargs):  # noqa: ARG001
    scheduler = ThreadedScheduler.get_instance()
    if instance.queue_watchdog is True:
        try:
            scheduler.every(1).seconds.do(QueueManager().schedule_jobs)
            scheduler.start()
        except Exception as e:
            print(e)
    else:
        try:
            scheduler.stop()
        except Exception as e:
            print(e)
