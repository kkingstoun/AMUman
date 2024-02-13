# Create your views here.
from typing import ClassVar

from rest_framework import permissions, viewsets

from .models import Gpus, Job, ManagerSettings, Nodes
from .serializers import GpusSerializer, JobSerializer, MSSerializer, NodesSerializer


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]


class GpusViewSet(viewsets.ModelViewSet):
    queryset = Gpus.objects.all()
    serializer_class = GpusSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]


class NodesViewSet(viewsets.ModelViewSet):
    queryset = Nodes.objects.all()
    serializer_class = NodesSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]


class ManagerSettingsViewSet(viewsets.ModelViewSet):
    queryset = ManagerSettings.objects.all()
    serializer_class = MSSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]
