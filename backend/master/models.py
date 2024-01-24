from django.db import models

class Task(models.Model):
    path = models.CharField(max_length=500)
    node_name = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)  # Dodaj to pole
    status = models.CharField(max_length=50, default='waiting')  # ['waiting', 'running', 'finished']

class Nodes(models.Model):
    ip = models.CharField(max_length=15)
    port = models.CharField(max_length=5)
    gpu_info = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ip}:{self.port}"