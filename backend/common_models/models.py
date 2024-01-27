from django.db import models
from django.utils import timezone
class Task(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generowany unikalny klucz
    user = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=500)
    node_name = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)
    priority = models.IntegerField(default=0)  
    gpu_partition = models.CharField(max_length=15, unique=True, null=True, blank=True, default='normal')
    est = models.DurationField(null=True, blank=True)
    status = models.CharField(max_length=50, default='waiting')  # ['waiting', 'running', 'finished']
    assigned_node= models.CharField(max_length=10, null=True,blank=True)
    assigned_gpu= models.CharField(max_length=10,null=True, blank=True)

    
class Nodes(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-generowany unikalny klucz
    ip = models.CharField(max_length=15, unique=True)  # Przykładowy format IPv4
    name = models.CharField(max_length=15, unique=True,null=True, blank=True)  # Przykładowy format IPv4
    port = models.IntegerField(null=True, blank=True)
    number_of_gpus = models.CharField(max_length=15, null=True,blank=True)
    gpu_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default='free')  # np. 'active', 'disconnected'
    last_seen = models.DateTimeField(default=timezone.now,null=True, blank=True)

    def __str__(self):
        return f"{self.ip}:{self.port} - {self.status}"
    
class Gpus(models.Model):
    id = models.AutoField(primary_key=True)  
    gpu_id = models.CharField(max_length=2,unique=True,default=0)
    node_id = models.ForeignKey(Nodes, on_delete=models.CASCADE)  
    brand_name = models.TextField(null=True, blank=True)
    gpu_speed = models.TextField(null=True, blank=True)
    gpu_util = models.TextField(null=True, blank=True)
    is_running_amumax = models.TextField(null=True, blank=True)
    gpu_info = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, default='free')  
    last_update = models.DateTimeField(default=timezone.now,null=True, blank=True)

    def __str__(self):
        return f"GPU-{self.id}, {self.node_id}/{self.gpu_id}"