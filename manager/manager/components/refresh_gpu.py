import time
from venv import logger

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.response import Response

from manager.models import Gpu


class RunJob:
    def __init__(self) -> None:
        self.time_break = 5

    def find_gpus(self):
        return Gpu.objects.all()

    def check_connection(self, gpu):
        for _ in range(5):
            if gpu.node.connection_status == "CONNECTED":
                return True
            else:
                print(
                    f"Node {gpu.node.name} is not connected. Attempting to reconnect in {self.time_break} seconds..."
                )
                time.sleep(self.time_break)
                self.time_break += 5  # Zwiększenie opóźnienia dla kolejnej próby

        # Jeśli pętla zakończy się bez powodzenia, logujemy błąd
        logger.error(f"Node {gpu.node.name} is not connected after multiple attempts.")
        return False

    def refres_gpus(self, gpu=None, request=None):
        try:
            if gpu!=None:
                for gpu in self.find_gpus():
                    if self.check_connection(gpu):
                        self.send_run_command(gpu)
            else:
                self.send_run_command(gpu)    

        except Exception as e:
            time.sleep(self.time_break)
            self.time_break += 5

            if request is not None:
                return self.handle_response(request, str(e), "danger", 400)
            else:
                print(f"run_job: {e}")
                logger.error(e)

    def send_run_command(self,gpu):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "nodes_group",  # Assume a group name for nodes
                {
                    "type": "node.command",
                    "command": "refresh_gpu",
                    "node_id": gpu.node.pk,
                    "gpu_device_id": gpu.device_id,
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

