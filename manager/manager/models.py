from enum import Enum

from django.db import models
from django.utils import timezone


class Node(models.Model):
    class NodeStatus(Enum):
        WAITING = "Waiting"
        RUNNING = "Running"
        RESERVED = "Reserved"
        UNAVAILABLE = "Unavailable"

    class ConnectionStatus(Enum):
        CONNECTED = "Connected"
        DISCONNECTED = "Disconnected"

    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=15, unique=True)
    number_of_gpus = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in NodeStatus],
        default=NodeStatus.WAITING.name,
    )
    connection_status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in ConnectionStatus],
        default=ConnectionStatus.CONNECTED.name,
    )
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Gpu(models.Model):
    class GPUStatus(Enum):
        WAITING = "Waiting"
        RUNNING = "Running"
        RESERVED = "Reserved"
        UNAVAILABLE = "Unavailable"

    class GPUSpeed(Enum):
        SLOW = "Slow"
        NORMAL = "Normal"
        FAST = "Fast"

    device_id = models.PositiveSmallIntegerField()
    uuid = models.UUIDField(unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    model = models.TextField()
    speed = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in GPUSpeed],
        default=GPUSpeed.NORMAL.name,
    )
    util = models.PositiveSmallIntegerField()
    is_running_amumax = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in GPUStatus],
        default=GPUStatus.WAITING.name,
    )
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"GPU-{self.id}, {self.node}/{self.id}"


class Job(models.Model):
    class JobPriority(Enum):
        LOW = "Low"
        NORMAL = "Normal"
        HIGH = "High"

    class JobStatus(Enum):
        WAITING = "Waiting"
        PENDING = "Pending"
        RUNNING = "Running"
        FINISHED = "Finished"
        INTERRUPTED = "Interrupted"

    class GPUPartition(Enum):
        SLOW = "Slow"
        NORMAL = "Normal"
        FAST = "Fast"

    path = models.CharField(max_length=500)
    port = models.PositiveIntegerField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=6,
        choices=[(choice.name, choice.value) for choice in JobPriority],
        default=JobPriority.NORMAL.name,
    )
    gpu_partition = models.CharField(
        max_length=6,
        choices=[(choice.name, choice.value) for choice in GPUPartition],
        default=GPUPartition.NORMAL.name,
    )
    estimated_simulation_time = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in JobStatus],
        default=JobStatus.WAITING.name,
    )
    node = models.ForeignKey(
        Node, on_delete=models.SET_NULL, null=True, blank=True, related_name="node"
    )
    gpu = models.ForeignKey(
        Gpu, on_delete=models.SET_NULL, null=True, blank=True, related_name="job"
    )
    output = models.TextField(null=True, blank=True)
    error = models.TextField(null=True, blank=True)
    flags = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return f"{self.id}:{self.path[-50:]}"


class ManagerSettings(models.Model):
    queue_watchdog = models.BooleanField(default=False)
