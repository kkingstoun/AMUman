# Create your views here.
import logging
import time
from typing import ClassVar
from venv import logger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .components.run_job import RunJob
from .models import CustomUser, Gpu, Job, Node
from .serializers import (
    CustomUserSerializer,
    GpuSerializer,
    JobSerializer,
    NodeSerializer,
    RefreshNodeSerializer,
)

log = logging.getLogger("rich")


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "priority", "node", "gpu", "status"]

    def retrieve(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"action": self.action})
        return Response(serializer.data)

    def create(self, request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            log.debug(f"Job created: {serializer.data}")
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as e:
            log.error(f"Job not created: {e}")
            return Response(
                f"Job not created: {e}",
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers,
            )

    def update(self, request, *args, **kwargs):
        print(request.data)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def start(self, _request, pk=None):
        try:
            job = self.get_object()
            gpu = Gpu.objects.filter(status="PENDING").first()
            if not gpu:
                return Response(
                    {"error": "Gpu unavailable."}, status=status.HTTP_400_BAD_REQUEST
                )

            self.rt = RunJob()
            self.rt.run_job(job=job, request=_request)

            return Response(
                {"message": f"Job {pk} started successfully."},
                status=status.HTTP_200_OK,
            )
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND
            )


class GpusViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    queryset = Gpu.objects.all()
    serializer_class = GpuSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]

    def create(self, request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                gpu, created = Gpu.objects.update_or_create(
                    uuid=serializer.validated_data["uuid"],
                    defaults=serializer.validated_data,
                )
                if created:
                    # headers = self.get_success_headers(serializer.data) #TODO: check if this is needed
                    return Response(
                        {
                            "message": f"Gpu sucessfull assigned. Your node_id is: {gpu.device_id}",
                            "device_id": gpu.device_id,
                        },
                        status=status.HTTP_201_CREATED,
                    )

        except ValidationError as e:
            logger.error(f"GPU not created: {e}")
            if "uuid" in serializer.errors and "already exists" in str(
                serializer.errors["uuid"]
            ):
                gpu = Gpu.objects.get(uuid=request.data["uuid"])
                update_serializer = self.get_serializer(
                    gpu, data=request.data, partial=True
                )
                update_serializer.is_valid(raise_exception=True)
                self.perform_update(update_serializer)
                return Response(update_serializer.data)
            else:
                return Response(
                    {
                        "message": f"Gpu not assigned. Error: {e}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

    @action(detail=True, methods=["post"])
    def refresh(self, _request):
        try:
            return Response(
                {"message": "Gpus updated."},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response({"error": "{e}"}, status=status.HTTP_404_NOT_FOUND)


class NodesViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    @action(
        detail=False,
        methods=["post"],
        url_path="refresh",
        serializer_class=RefreshNodeSerializer,
    )
    def refreshnode(self, request):
        node_id = request.data.get("node_id", None)
        channel_layer = get_channel_layer()
        if channel_layer and node_id:
            async_to_sync(channel_layer.group_send)(
                "nodes_group",
                {
                    "type": "node.command",
                    "command": "update_gpus",
                    "node_id": node_id,
                },
            )
            async_to_sync(channel_layer.group_send)(
                "nodes_group",
                {
                    "type": "node.command",
                    "command": "update_gpus",
                    "node_id": None,
                },
            )
        time.sleep(3)
        return Response({"status": "Command sent"}, status=status.HTTP_200_OK)

    def create(self, request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            node, created = Node.objects.get_or_create(
                name=request.data.get("name"), defaults=request.data
            )
            if created:
                headers = self.get_success_headers(serializer.data)
                return Response(
                    {
                        "message": f"Node assigned. Your node_id is: {node.pk}",
                        "id": node.pk,
                    },
                    status=status.HTTP_201_CREATED,
                    headers=headers,
                )
            else:
                serializer = self.get_serializer(node, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(
                    {
                        "message": f"Node already exists. Your node_id is: {node.pk}",
                        "id": node.pk,
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            log.info("Node reconnected")
            if (
                "name" in serializer.errors
                and "unique" in serializer.errors["name"][0].code
            ):
                node = Node.objects.get(name=request.data.get("name"))
                return Response(
                    {
                        "message": f"Node already exists. Your node_id is: {node.pk}",
                        "id": node.pk,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
