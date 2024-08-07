import logging
import time
from typing import ClassVar
from venv import logger

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from manager.components.check_mx3_file import validate_mx3_file
from manager.components.ws_messages import WebsocketMessage, send_message

from .components.run_job import run_job
from .models import CustomUser, Gpu, Job, Node
from .serializers import (
    BenchNodeSerializer,
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
        return [permissions.IsAuthenticated()]

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

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, _request, *_args, **_kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"action": self.action})
        return Response(serializer.data)

    def create(self, request, *_args, **_kwargs):
        # Modify the request data to include the user
        custom_user = CustomUser.objects.get(auth=request.user)
        modified_data = request.data.copy()
        modified_data["username"] = custom_user.auth.username
        modified_data["user"] = custom_user.pk
        modified_data["submit_time"] = timezone.now()
        log.debug(f"Modified data: {modified_data}")
        # Now, proceed with serialization and saving as before
        serializer = self.get_serializer(data=modified_data)
        try:
            serializer.is_valid(raise_exception=True)
            if not validate_mx3_file(serializer.validated_data["path"]):
                log.error("Job not created: Invalid file path")
                return Response(
                    {"detail": "Invalid file path"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            log.debug(f"Job created: {serializer.data}")
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except ValidationError as e:
            log.error(f"Job not created: {e}")
            # If headers is not defined before the try-except block, it should be moved inside the try block or defined before it
            return Response(
                {"detail": str(e)},  # It's better to return structured error responses
                status=status.HTTP_400_BAD_REQUEST,
            )

    def update(self, request, *args, **kwargs):
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

            run_job(job=job)

            return Response(
                {"message": f"Job {pk} started successfully."},
                status=status.HTTP_200_OK,
            )
        except Job.DoesNotExist:
            return Response(
                {"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND
            )


class GpusViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "put"]
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


class NodesViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete", "put"]
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]


    @action(
        detail=False,
        methods=["post"],
        url_path="refresh",
        serializer_class=RefreshNodeSerializer,
    )
    def refresh_node(self, request):
        node_id = request.data.get("node_id", None)
        send_message(
            WebsocketMessage(
                command="update_gpus",
                node_id=node_id,
            )
        )
        time.sleep(3)
        return Response({"status": "Command sent"}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["post"],
        url_path="bench",
        serializer_class=BenchNodeSerializer,
    )
    def bench_node(self, request):
        node_id = request.data.get("node_id", None)
        send_message(
            WebsocketMessage(
                command="bench_gpus",
                node_id=node_id,
            )
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
