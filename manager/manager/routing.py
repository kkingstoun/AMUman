from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    GpusViewSet,
    JobsViewSet,
    NodesViewSet,
)

manager_router = DefaultRouter()

manager_router.register(r"jobs", JobsViewSet, basename="job")
manager_router.register(r"nodes", NodesViewSet, basename="node")
manager_router.register(r"gpus", GpusViewSet, basename="gpu")
manager_router.register(r"users", CustomUserViewSet, basename="user")
