import time
from venv import logger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework.response import Response

from manager.models import Gpu


class RunJob:
    def __init__(self) -> None:
        self.time_break = 5
        
    def find_gpu(self, partition):
        gpu = Gpu.objects.filter(status="Waiting", 
                                #  speed=partition                 #TEMPORARY DISABLED
                                 ).first()
        if gpu is None:
            time.sleep(self.time_break)
            self.time_break += 5
            print(f"No available GPU in the {partition} partition.")
            logger.error(f"No available GPU in the {partition} partition.")
            return None
        return gpu

    def run_job(self, job=None, gpu=None, request=None):
        try:
            if gpu is None:
                gpu = self.find_gpu(job.gpu_partition)
                if gpu.node.status != "Connected":
                    time.sleep(self.time_break)
                    self.time_break += 5
                    print(f"Node {gpu.node.name} is not connected.")
                    logger.error(f"Node {gpu.node.name} is not connected.")
                    return self.handle_response(
                        request,
                        f"Node {gpu.node.name} is not connected.",
                        "danger",
                        400,
                    )
            # Send job run command to the node managing the selected GPU
            job.node=gpu.node
            job.gpu=gpu
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
        
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "nodes_group",  # Assume a group name for nodes
                {
                    "type": "node.command",
                    "command": "run_job",
                    "node_id": job.gpu.node.pk,
                    "job_id": job.pk,
                    "gpu_device_id": job.gpu.device_id,
                },
            )
        except Exception as e:
            print(f"send_run_command: {e}")
            logger.error(e)
            
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
