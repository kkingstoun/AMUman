
# Create your views here.
from typing import ClassVar

from rest_framework import generics, permissions, viewsets

from .models import Task
from .serializers import TaskSerializer

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task, Nodes
# from .forms import TaskForm, NodeForm


class TasksViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]

class GpusViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]

class NodesViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]

class ManagerSettingsViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]


class MessageCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post']

class MessageListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class =  TaskSerializer
    http_method_names = ['get']


    