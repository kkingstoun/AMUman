import logging
from typing import Tuple

from rest_framework.response import Response

from manager.components.ws_messages import WebsocketMessage, send_message
from manager.models import Gpu, Job, Node
from django.utils import timezone

log = logging.getLogger("rich")


def run_job(job: Job, gpu: Gpu | None = None) -> Response:
    if gpu is None:
        gpu, res = find_gpu(job.gpu_partition)
        if res is not None:
            return res
    if gpu is None:
        log.error("No available GPU.")
        return Response(
            {"message": "No available GPU."},
            status=400,
        )
    if gpu.node.connection_status == "CONNECTED":
        job.node = gpu.node
        job.gpu = gpu

        job.status = Job.JobStatus.RUNNING.value
        job.start_time = timezone.now()
        job.save()

        if send_run_command(job):
            gpu.status = Gpu.GPUStatus.RUNNING.value
            gpu.node.status = Node.NodeStatus.RESERVED.value
            node = Node.objects.filter(
                ip = gpu.node.ip
            ).first()
            node.status = Node.NodeStatus.RESERVED.value
            #log.debug("!!!!! status node: ", gpu.node.status, "job:",job.node.id )
            gpu.last_update = job.start_time

            gpu.save()
            node.save()
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
        if job.node is None or job.gpu is None:
            log.error("Job does not have a node or GPU assigned.")
            return False
        msg = WebsocketMessage(
            command="run_job",
            node_id=job.node.pk,
            job_id=job.pk,
            gpu_device_id=job.gpu.device_id,
        )
        log.debug(f"Sending run command for job {job.pk}")
        send_message(msg)
        return True
    except Exception as e:
        log.debug(f"send_run_command: {e}")
        return False


def find_gpu(_partition: str) -> Tuple[Gpu | None, Response | None]:
    # TODO: Filter by partition
    gpu = Gpu.objects.filter(
        status="PENDING",
    ).first()
    if gpu is None:
        log.error("No available GPU.")
        return None, Response(
            {"message": "No available GPU."},
            status=400,
        )
    if gpu.node.connection_status == "CONNECTED":
        log.debug(f"Found GPU {gpu.device_id}.")
        return gpu, None
    else:
        log.error(f"Node {gpu.node.pk} is not connected.")
        return None, Response(
            {"message": f"Node {gpu.node.pk} is not connected."}, status=400
        )
