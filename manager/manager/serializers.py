from rest_framework import serializers

from .models import Gpu, Job, ManagerSettings, Node

# https://www.django-rest-framework.org/api-guide/serializers/#modelserializer


class NodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class GpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gpu
        fields = "__all__"


class MSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSettings
        fields = "__all__"
