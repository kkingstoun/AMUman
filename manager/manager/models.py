from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Node(models.Model):
    class NodeStatus(Enum):
        Waiting = "Waiting"
        Running = "Running"
        Reserved = "Reserved"
        Unavailable = "Unavailable"

    class ConnectionStatus(Enum):
        Connected = "Connected"
        Disconnected = "Disconnected"

    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=15, unique=True)
    number_of_gpus = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in NodeStatus],
        default=NodeStatus.Waiting.name,
    )
    connection_status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in ConnectionStatus],
        default=ConnectionStatus.Connected.name,
    )
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class Gpu(models.Model):
    class GPUStatus(models.TextChoices):
        Waiting = 'Waiting', _('Waiting')
        Running = 'Running', _('Running')
        Reserved = 'Reserved', _('Reserved')
        Unavailable = 'Unavailable', _('Unavailable')

    class GPUSpeed(models.TextChoices):
        Slow = 'Slow', _('Slow')
        Normal = 'Normal', _('Normal')
        Fast = 'Fast', _('Fast')

    device_id = models.PositiveSmallIntegerField()
    uuid = models.UUIDField(unique=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    model = models.TextField()
    speed = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in GPUSpeed],
        default=GPUSpeed.Normal.name,
    )
    util = models.PositiveSmallIntegerField()
    is_running_amumax = models.BooleanField(default=False)
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in GPUStatus],
        default=GPUStatus.Waiting.name,
    )
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"GPU-{self.id}, {self.node}/{self.id}"


class Job(models.Model):
    class JobPriority(Enum):
        LOW = "Low"
        Normal = "Normal"
        HIGH = "High"

    class JobStatus(Enum):
        Waiting = "Waiting"
        Pending = "Pending"
        Running = "Running"
        Finished = "Finished"
        Interrupted = "Interrupted"

    class GPUPartition(Enum):
        Slow = "Slow"
        Normal = "Normal"
        Fast = "Fast"

    path = models.CharField(max_length=500)
    port = models.PositiveIntegerField(null=True, blank=True)
    submit_time = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    error_time = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=6,
        choices=[(choice.name, choice.value) for choice in JobPriority],
        default=JobPriority.Normal.name,
    )
    gpu_partition = models.CharField(
        max_length=6,
        choices=[(choice.name, choice.value) for choice in GPUPartition],
        default=GPUPartition.Normal.name,
    )
    duration = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in JobStatus],
        default=JobStatus.Waiting.name,
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
    user = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.id}:{self.path[-50:]}"


class ManagerSettings(models.Model):
    queue_watchdog = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    concurrent_jobs = models.IntegerField(
        default=0, choices=[(x, str(x)) for x in range(11)]
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(_sender, instance, created, **_kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
