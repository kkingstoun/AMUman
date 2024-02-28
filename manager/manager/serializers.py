from django.core.validators import MaxValueValidator
from django.utils import timezone
from rest_framework import serializers

from .models import Gpu, Job, ManagerSettings, Node


class NodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class RefreshNodeSerializer(serializers.Serializer):
    node_id = serializers.IntegerField(required=False)


class GpusSerializer(serializers.ModelSerializer):
    speed = serializers.ChoiceField(
        choices=Gpu.GPUSpeed.choices,
        default=Gpu.GPUSpeed.Normal,
        help_text='The speed of the GPU.'
    )
    status = serializers.ChoiceField(
        choices=Gpu.GPUStatus.choices,
        default=Gpu.GPUStatus.Waiting,
        help_text='The current status of the GPU.'
    )
    node = serializers.PrimaryKeyRelatedField(
        queryset=Node.objects.all(), help_text="The associated node ID."
    )

    class Meta:
        model = Gpu
        fields = "__all__"
        extra_kwargs = {
            "device_id": {
                "validators": [MaxValueValidator(32767)],
                "help_text": "The unique device identifier (must be <= 32767).",
            },
            "util": {
                "validators": [MaxValueValidator(100)],
                "help_text": "The utilization of the GPU (must be <= 100).",
            },
            "uuid": {"help_text": "The unique identifier of the GPU."},
            "last_update": {
                "read_only": True,
                "default": serializers.CreateOnlyDefault(timezone.now),
                "help_text": "The timestamp of the last update (read-only, auto-generated).",
            },
        }

    def to_representation(self, instance):
        """
        Because the `node` field is a ForeignKey, we want to display the node's string representation,
        which might be more useful in the API response than just the ID.
        """
        ret = super().to_representation(instance)
        if "node" in ret:
            node_instance = Node.objects.get(pk=ret["node"])
            ret["node"] = str(node_instance)

        return ret

    def create(self, validated_data):
        gpu, created = Gpu.objects.get_or_create(
            uuid=validated_data.get("uuid"), defaults=validated_data
        )
        if not created:
            return self.update(gpu, validated_data)
        return gpu

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def save(self, **kwargs):
        uuid = self.validated_data.get("uuid")
        gpu = Gpu.objects.filter(uuid=uuid).first()

        if gpu is not None:
            return self.update(gpu, self.validated_data)
        else:
            return super().save(**kwargs)


class MSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerSettings
        fields = "__all__"
