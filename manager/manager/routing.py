from django.contrib.auth.models import User
from django.urls import path
from rest_framework import serializers, viewsets
from rest_framework.routers import DefaultRouter

from .consumers import ManagerConsumer
from .views import GpusViewSet, JobsViewSet, ManagerSettingsViewSet, NodesViewSet

# Tworzenie instancji DefaultRouter
manager_router = DefaultRouter()

# Rejestracja viewsets z odpowiednimi endpointami
manager_router.register(r"jobs", JobsViewSet, basename="job")
manager_router.register(r"nodes", NodesViewSet, basename="node")
manager_router.register(r"gpus", GpusViewSet, basename="gpu")
manager_router.register(
    r"manager-settings", ManagerSettingsViewSet, basename="manager-settings"
)


websocket_urlpatterns = [
    path("ws/node", ManagerConsumer.as_asgi()),
]


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
manager_router.register(r"users", UserViewSet)
