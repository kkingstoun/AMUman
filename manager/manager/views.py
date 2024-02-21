# Create your views here.
import logging
from typing import ClassVar

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Gpu, Job, ManagerSettings, Node
from .serializers import GpusSerializer, JobSerializer, MSSerializer, NodesSerializer

log = logging.getLogger("rich")


class JobsViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    # permission_classes: ClassVar = [permissions.IsAuthenticated]

    def list(self, request, *_args, **_kwargs):
        max_id = request.query_params.get("max_id")
        if max_id is not None:
            queryset = self.queryset.filter(id__lt=max_id)
        else:
            queryset = self.get_queryset()
        return Response(JobSerializer(queryset, many=True).data)

    def retrieve(self, _request, *_args, **_kwargs):
        data = JobSerializer(instance=self.get_object()).data
        data["user"] = "hsi"
        return Response(data)

    def create(self, request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        log.debug(f"Job created: {serializer.data}")
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        try:
            job = self.get_object()
            job.status = Job.JobStatus.RUNNING.name
            job.save()
            return Response({"message": f"Job {pk} started successfully."}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)




class GpusViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get"]
    queryset = Gpu.objects.all()
    serializer_class = GpusSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                gpu, created = Gpu.objects.update_or_create(
                            uuid=serializer.validated_data['uuid'],
                            defaults=serializer.validated_data
                        )
                if created:
                    headers = self.get_success_headers(serializer.data)
                    return Response({'message': f'Gpu sucessfull assigned. Your node_id is: {gpu.device_id}', 'device_id': gpu.device_id}, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Sprawdź, czy błąd jest związany z istniejącym UUID
            if 'uuid' in serializer.errors and 'already exists' in str(serializer.errors['uuid']):
                gpu = Gpu.objects.get(uuid=request.data['uuid'])
                update_serializer = self.get_serializer(gpu, data=request.data, partial=True)
                update_serializer.is_valid(raise_exception=True)
                self.perform_update(update_serializer)
                return Response(update_serializer.data)
            else:
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         gpu, created = Gpu.objects.update_or_create(
    #             uuid=serializer.validated_data['uuid'],
    #             defaults=serializer.validated_data
    #         )
    #         if created:
    #             headers = self.get_success_headers(serializer.data)
    #             return Response({'message': f'Gpu sucessfull assigned. Your node_id is: {gpu.device_id}', 'device_id': gpu.device_id}, status=status.HTTP_201_CREATED)
    #             # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #         else:
    #             return Response({'message': f'Gpu already exists. Your gpu_id is: {gpu.device_id}', 'device_id': gpu.device_id}, status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NodesViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodesSerializer
    permission_classes: ClassVar = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            node, created = Node.objects.get_or_create(
                name=request.data.get('name'),
                defaults=request.data
            )
            if created:
                headers = self.get_success_headers(serializer.data)
                return Response({'message': f'Node assigned. Your node_id is: {node.id}', 'id': node.id}, status=status.HTTP_201_CREATED, headers=headers)
            else:
                serializer = self.get_serializer(node, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'message': f'Node already exists. Your node_id is: {node.id}', 'id': node.id}, status=status.HTTP_200_OK)
        else:
            log.info("Node reconnected")
            if 'name' in serializer.errors and 'unique' in serializer.errors['name'][0].code:
                node = Node.objects.get(name=request.data.get('name'))
                return Response({'message': f'Node already exists. Your node_id is: {node.id}', 'id': node.id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ManagerSettingsViewSet(viewsets.ModelViewSet):
    queryset = ManagerSettings.objects.all()
    serializer_class = MSSerializer
    # permission_classes: ClassVar = [permissions.IsAuthenticated]

