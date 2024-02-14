# Create your models here.
from django.db import models
from django.utils import timezone


class Node(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    ip = models.CharField(max_length=15)  # Przykładowy format IPv4
    name = models.CharField(max_length=15, unique=True)  # Przykładowy format IPv4
    # port = models.IntegerField(null=True, blank=True)
    number_of_gpus = models.CharField(max_length=15)
    # gpu_info = models.TextField(null=True, blank=True)
    STATUS_CHOICES = [
        ("Waiting", "Waiting"),
        ("Running", "Running"),
        ("Reserved", "Reserved"),
        ("Unavailable", "Unavailable"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Waiting")
    CONNECTION_CHOICES = [
        ("Connected", "Connected"),
        ("Disconnected", "Disconnected"),
    ]
    connection_status = models.CharField(
        max_length=50, choices=CONNECTION_CHOICES, default="Connected"
    )
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Job(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    user = models.CharField(max_length=100, null=True, blank=True)
    path = models.CharField(max_length=500)
    node_name = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)

    PRIORITY_CHOICES = [("Low", "Low"), ("Normal", "Normal"), ("High", "High")]
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="Normal"
    )

    GPU_PARTITION_CHOICES = [("Slow", "Slow"), ("Normal", "Normal"), ("Fast", "Fast")]
    gpu_partition = models.CharField(
        max_length=6, choices=GPU_PARTITION_CHOICES, default="Normal"
    )
    estimated_simulation_time = models.IntegerField(default=1)
    STATUS_CHOICES = [
        ("Waiting", "Waiting"),
        ("Pending", "Pending"),
        ("Running", "Running"),
        ("Finished", "Finished"),
        ("Interrupted", "Interrupted"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Waiting")
    assigned_gpu_id = models.CharField(max_length=10, null=True, blank=True)
    node = models.ForeignKey(Node, on_delete=models.SET_NULL, null=True, blank=True)
    output = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    flags = models.JSONField(default=dict, null=True, blank=True)

    def __str__(self):
        return f"{self.user}:{self.path[-50:]}"


class Gpu(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    device_id = models.IntegerField(unique=True)
    uuid = models.TextField(unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    model = models.TextField()
    STATUS_CHOICES = [
        ("Slow", "Slow"),
        ("Normal", "Normal"),
        ("Fast", "Fast"),
    ]
    speed = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Normal")

    util = models.IntegerField()
    is_running_amumax = models.BooleanField()
    # info = models.TextField(null=True, blank=True)

    STATUS_CHOICES = [
        ("Waiting", "Waiting"),
        ("Running", "Running"),
        ("Reserved", "Reserved"),
        ("Unavailable", "Unavailable"),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Waiting")
    last_update = models.DateTimeField(default=timezone.now)
    job = models.ForeignKey(
        Job, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu"
    )

    def __str__(self):
        return f"GPU-{self.id}, {self.node}/{self.id}"


class ManagerSettings(models.Model):
    # id = models.AutoField(primary_key=True, unique=True)
    queue_watchdog = models.BooleanField(default=False)
