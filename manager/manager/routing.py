from django.urls import path
from rest_framework.routers import DefaultRouter

from .consumers import ManagerConsumer
from .views import GpusViewSet, ManagerSettingsViewSet, NodesViewSet, TasksViewSet

# Tworzenie instancji DefaultRouter
manager_router = DefaultRouter()

# Rejestracja viewsets z odpowiednimi endpointami
manager_router.register(r'tasks', TasksViewSet, basename='task')
manager_router.register(r'nodes', NodesViewSet, basename='node')
manager_router.register(r'gpus', GpusViewSet, basename='gpu')
manager_router.register(r'manager-settings', ManagerSettingsViewSet, basename='manager-settings')



websocket_urlpatterns = [
    path("ws/node", ManagerConsumer.as_asgi()),
]
