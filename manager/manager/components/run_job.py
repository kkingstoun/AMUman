import time
from venv import logger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework.response import Response


class RunJob:
    def __init__(self) -> None:
        self.time_break = 5
        pass

    def run_job(self, job=None, gpu=None, request=None):
        try:
            gpu.status = "Running"
            gpu.job_id = job
            gpu.last_update = timezone.now()
            gpu.save()

            # Update job with assigned GPU and status
            job.assigned_gpu_id = gpu.no
            job.assigned_node_id = gpu.node_id.id
            job.status = "Running"
            job.submit_time = timezone.now()
            job.save()

            # Send job run command to the node managing the selected GPU
            self.send_run_command(job, gpu)
            time.sleep(3)
            if request is not None:
                return self.handle_response(
                    request,
                    f"Job {gpu.job_id.id} is running on GPU {gpu.id}.",
                    "success",
                    200,
                )
        except Exception as e:
            time.sleep(self.time_break)
            self.time_break += 5

            if request is not None:
                return self.handle_response(request, str(e), "danger", 400)
            else:
                print(f"run_job: {e}")
                logger.error(e)

    def send_run_command(self, job, _gpu):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "nodes_group",  # Assume a group name for nodes
            {
                "type": "node.command",
                "command": "run_job",
                "node_id": job.assigned_node_id,
                "job_id": job.id,
                "gpu_id": job.assigned_gpu_id,
            },
        )

    def handle_response(self, request, message, tag, status_code=200):
        if (
            request.accepted_renderer.format == "json"
            or request.content_type == "application/json"
        ):
            response_content = (
                {"message": message} if status_code == 200 else {"error": message}
            )
            return Response(response_content, status=status_code)
        else:
            # Add message for HTML response
            from django.contrib import messages

            if tag == "success":
                messages.success(request, message)
            elif tag == "danger":
                messages.error(request, message)
            else:
                messages.info(request, message)
