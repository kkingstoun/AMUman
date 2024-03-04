from enum import Enum

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Node(models.Model):
    class NodeStatus(Enum):
        PENDING = "PENDING"
        RESERVED = "RESERVED"
        UNAVAILABLE = "UNAVAILABLE"

    class ConnectionStatus(Enum):
        CONNECTED = "CONNECTED"
        DISCONNECTED = "DISCONNECTED"

    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=15, unique=True)
    number_of_gpus = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in NodeStatus],
        default=NodeStatus.PENDING.name,
    )
    connection_status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in ConnectionStatus],
        default=ConnectionStatus.CONNECTED.name,
    )
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk}"


class Gpu(models.Model):
    class GPUStatus(Enum):
        RUNNING = "RUNNING"
        PENDING = "PENDING"
        RESERVED = "RESERVED"  # not implemented
        UNAVAILABLE = "UNAVAILABLE"  # High usage not from job or error

    class GPUSpeed(Enum):
        SLOW = "SLOW"
        NORMAL = "NORMAL"
        FAST = "FAST"

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
        default=GPUStatus.PENDING.name,
    )
    last_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.pk}"


class Job(models.Model):
    class JobPriority(Enum):
        LOW = "LOW"
        NORMAL = "NORMAL"
        HIGH = "HIGH"

    class JobStatus(Enum):
        PENDING = "PENDING"
        FINISHED = "FINISHED"
        INTERRUPTED = "INTERRUPTED"

    class GPUPartition(Enum):
        SLOW = "SLOW"
        NORMAL = "NORMAL"
        FAST = "FAST"
        # This next field is only to remove the enum conflict with the GPU speed
        UNDEF = "UNDEF"

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
    duration = models.PositiveSmallIntegerField(default=1)
    status = models.CharField(
        max_length=50,
        choices=[(choice.name, choice.value) for choice in JobStatus],
        default=JobStatus.PENDING.name,
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
        return f"{self.pk}"


class ManagerSettings(models.Model):
    queue_watchdog = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and ManagerSettings.objects.exists():
            raise ValidationError("There can only be one entry of ManagerSettings.")
        return super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    concurrent_jobs = models.IntegerField(
        default=0, choices=[(x, str(x)) for x in range(11)]
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **_kwargs):  # noqa: ARG001
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
