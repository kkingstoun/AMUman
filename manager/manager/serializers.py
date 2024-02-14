from rest_framework import serializers

from .models import Gpu, Job, ManagerSettings, Node


class JobSerializer(serializers.ModelSerializer):
    # priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    # gpu_partition_display = serializers.CharField(source='get_gpu_partition_display', read_only=True)
    # status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Job
        fields = [
            "id",
            "user",
        ]
        read_only_fields = ("id",)


class GpusSerializer(serializers.ModelSerializer):
    # node_id = serializers.PrimaryKeyRelatedField(queryset=Nodes.objects.all())
    # gpu_speed_display = serializers.SerializerMethodField()
    # status_display = serializers.SerializerMethodField()

    class Meta:
        model = Gpu
        fields = [
            "device_id",
            "uuid",
        ]

    # def get_gpu_speed_display(self, obj):
    #     return obj.get_gpu_speed_display()

    # def get_status_display(self, obj):
    #     return obj.get_status_display()


class MSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSettings
        fields = ["queue_watchdog"]


class NodesSerializer(serializers.ModelSerializer):
    # status_display = serializers.SerializerMethodField()
    # connection_status_display = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = [
            "ip",
            "name",
        ]

    # def get_status_display(self, obj):
    #     return obj.get_status_display()

    # def get_connection_status_display(self, obj):
    #     return obj.get_connection_status_display()
