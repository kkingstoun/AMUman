
# Create your views here.
from typing import ClassVar

from rest_framework import permissions, viewsets

from .models import Gpus, ManagerSettings, Nodes, Task
from .serializers import GpusSerializer, MSSerializer, NodesSerializer, TaskSerializer

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
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




