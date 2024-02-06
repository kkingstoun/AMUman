from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    gpu_partition_display = serializers.CharField(source='get_gpu_partition_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'user', 'path', 'node_name', 'port', 'submit_time',
            'start_time', 'end_time', 'error_time', 'priority', 'gpu_partition',
            'est', 'status', 'assigned_node_id', 'assigned_gpu_id', 'output',
            'error', 'flags', 'priority_display', 'gpu_partition_display', 'status_display'
        ]
        read_only_fields = ('id',)  # Dodaj tutaj wszystkie pola, które mają być tylko do odczytu
