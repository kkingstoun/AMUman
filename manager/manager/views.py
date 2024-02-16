# Create your views here.
import logging

# from rest_framework import permissions
from rest_framework import status, viewsets
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


class GpusViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get"]
    queryset = Gpu.objects.all()
    serializer_class = GpusSerializer
    # permission_classes: ClassVar = [permissions.IsAuthenticated]


class NodesViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodesSerializer
    # permission_classes: ClassVar = [permissions.IsAuthenticated]


class ManagerSettingsViewSet(viewsets.ModelViewSet):
    queryset = ManagerSettings.objects.all()
    serializer_class = MSSerializer
    # permission_classes: ClassVar = [permissions.IsAuthenticated]
