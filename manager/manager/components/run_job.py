import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.response import Response

from manager.models import Gpu, Job

log = logging.getLogger("rich")


def run_job(job: Job, gpu: Gpu | None = None) -> Response:
    if gpu is None:
        gpu = find_gpu(job.gpu_partition)
        if gpu is None:
            log.error("No available GPU.")
            return Response(
                {"message": "No available GPU."},
                status=400,
            )
    if gpu.node.connection_status == "CONNECTED":
        job.node = gpu.node
        job.gpu = gpu
        job.save()
        if send_run_command(job):
            return Response(
                {
                    "message": f"Job {job.pk} has been scheduled to run on GPU {gpu.device_id}."
                },
                status=200,
            )
        else:
            log.error(f"Failed to send run command for job {job.pk}.")
            return Response(
                {"message": f"Failed to send run command for job {job.pk}."}, status=400
            )
    else:
        log.error(f"Node {gpu.node.pk} is not connected.")
        return Response(
            {"message": f"Node {gpu.node.pk} is not connected."}, status=400
        )


def send_run_command(job: Job) -> bool:
    try:
        channel_layer = get_channel_layer()
        if job.node is None or job.gpu is None:
            log.error("Job does not have a node or GPU assigned.")
            return False
        if channel_layer is None:
            log.debug("Channel layer is not initialized.")
            return False
        async_to_sync(channel_layer.group_send)(
            "nodes_group",  # Assume a group name for nodes
            {
                "type": "node.command",
                "command": "run_job",
                "node_id": job.node.pk,
                "job_id": job.pk,
                "gpu_device_id": job.gpu.device_id,
            },
        )
        return True
    except Exception as e:
        log.debug(f"send_run_command: {e}")
        return False


def find_gpu(_partition: str) -> Gpu | None:
    # TODO: Filter by partition
    gpu = Gpu.objects.filter(
        status="PENDING",
    ).first()
    if gpu is None:
        log.error("No available GPU.")
        return None
    return gpu
