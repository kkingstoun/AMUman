# scheduler/serializers.py

from rest_framework import serializers
from common_models.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
