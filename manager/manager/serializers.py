from rest_framework import serializers

from .models import Gpus, Job, ManagerSettings, Nodes


class JobSerializer(serializers.ModelSerializer):
    # priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    # gpu_partition_display = serializers.CharField(source='get_gpu_partition_display', read_only=True)
    # status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "user",
            "path",
            "node_name",
            "port",
            "submit_time",
            "start_time",
            "end_time",
            "error_time",
            "priority",
            "gpu_partition",
            "est",
            "status",
            "assigned_node_id",
            "assigned_gpu_id",
            "output",
            "error",
            "flags",
        ]
        read_only_fields = ("id",)


class GpusSerializer(serializers.ModelSerializer):
    node_id = serializers.PrimaryKeyRelatedField(queryset=Nodes.objects.all())
    gpu_speed_display = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Gpus
        fields = [
            "id",
            "no",
            "gpu_uuid",
            "node_id",
            "brand_name",
            "gpu_speed",
            "gpu_util",
            "is_running_amumax",
            "gpu_info",
            "status",
            "last_update",
            "job_id",
            "gpu_speed_display",
            "status_display",
        ]

    def get_gpu_speed_display(self, obj):
        return obj.get_gpu_speed_display()

    def get_status_display(self, obj):
        return obj.get_status_display()


class MSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSettings
        fields = ["id", "queue_watchdog"]


class NodesSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    connection_status_display = serializers.SerializerMethodField()

    class Meta:
        model = Nodes
        fields = [
            "id",
            "ip",
            "name",
            "port",
            "number_of_gpus",
            "gpu_info",
            "status",
            "connection_status",
            "last_seen",
            "status_display",
            "connection_status_display",
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()

    def get_connection_status_display(self, obj):
        return obj.get_connection_status_display()
