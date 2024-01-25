# scheduler/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Node

@shared_task
def check_node_status():
    now = timezone.now()
    for node in Node.objects.all():
        if now - node.last_seen > timezone.timedelta(minutes=1):
            node.status = 'disconnected'
            node.save()
        # Możesz dodać więcej logiki w zależności od wymagań
