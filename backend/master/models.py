from django.db import models
from django.utils import timezone
class Nodes(models.Model):
    ip = models.CharField(max_length=15, unique=True)  # Przykładowy format IPv4
    port = models.IntegerField(null=True, blank=True)
    gpu_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default='free')  # np. 'active', 'disconnected'
    last_seen = models.DateTimeField(default=timezone.now,null=True, blank=True)
    
    def __str__(self):
        return f"{self.ip}:{self.port} - {self.status}"