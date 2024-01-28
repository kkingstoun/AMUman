from django.db import models
from django.utils import timezone


class Task(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True
    )  # Auto-generowany unikalny klucz
    user = models.CharField(max_length=100, null=True, blank=True)
    path = models.TextField(null=False, blank=False)
    node_name = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)
    
    PRIORITY_CHOICES = [
        ('slow', 'Slow'),
        ('normal', 'Normal'),
        ('fast', 'Fast')
    ]
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    
    GPU_PARTITION_CHOICES = [
        ('slow', 'Slow'),
        ('normal', 'Normal'),
        ('fast', 'Fast')
    ]
    gpu_partition = models.CharField(
        max_length=6,
        choices=GPU_PARTITION_CHOICES,
        default='normal'
    )
    est = models.DurationField(null=True, blank=True)
    status = models.CharField(
        max_length=50, default="waiting"
    )  # ['waiting', 'running', 'finished']
    assigned_node = models.CharField(max_length=10, null=True, blank=True)
    assigned_gpu = models.CharField(max_length=10, null=True, blank=True)


class Nodes(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generowany unikalny klucz
    ip = models.CharField(max_length=15, unique=True)  # Przykładowy format IPv4
    name = models.CharField(
        max_length=15, unique=True, null=True, blank=True
    )  # Przykładowy format IPv4
    port = models.IntegerField(null=True, blank=True)
    number_of_gpus = models.CharField(max_length=15, null=True, blank=True)
    gpu_info = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=10, default="free"
    )  # np. 'active', 'disconnected'
    last_seen = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.ip}:{self.port} - {self.status}"


class Gpus(models.Model):
    id = models.AutoField(
        primary_key=True, unique=True
    )
    gpu_uuid=models.TextField(unique=True,null=True, blank=True)
    node_id = models.ForeignKey(Nodes, on_delete=models.CASCADE)
    brand_name = models.TextField(null=True, blank=True)
    gpu_speed = models.TextField(null=True, blank=True)
    gpu_util = models.TextField(null=True, blank=True)
    is_running_amumax = models.TextField(null=True, blank=True)
    gpu_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default="free")
    last_update = models.DateTimeField(default=timezone.now, null=True, blank=True)
    task_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"GPU-{self.id}, {self.node_id}/{self.id}"
