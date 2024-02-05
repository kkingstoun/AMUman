import time
from venv import logger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from rest_framework.response import Response


class RunTask:
    def __init__(self) -> None:
        self.time_break = 5
        pass

    def run_task(self, task=None, gpu=None, request=None):
        try:
            gpu.status = "Running"
            gpu.task_id = task
            gpu.last_update = timezone.now()
            gpu.save()

            # Update task with assigned GPU and status
            task.assigned_gpu_id = gpu.no
            task.assigned_node_id = gpu.node_id.id
            task.status = "Running"
            task.submit_time = timezone.now()
            task.save()

            # Send task run command to the node managing the selected GPU
            self.send_run_command(task, gpu)
            time.sleep(3)
            if request is not None:
                return self.handle_response(
                    request,
                    f"Task {gpu.task_id.id} is running on GPU {gpu.id}.",
                    "success",
                    200,
                )
        except Exception as e:
            time.sleep(self.time_break)
            self.time_break += 5

            if request is not None:
                return self.handle_response(request, str(e), "danger", 400)
            else:
                print(f"run_task: {e}")
                logger.error(e)

    def send_run_command(self, task, gpu):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "nodes_group",  # Assume a group name for nodes
            {
                "type": "node.command",
                "command": "run_task",
                "node_id": task.assigned_node_id,
                "task_id": task.id,
                "gpu_id": task.assigned_gpu_id,
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
