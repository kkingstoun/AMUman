import asyncio
import json
import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from manager.components.ws_messages import WebsocketMessage, parse_message
from manager.models import Job, Node, Gpu

log = logging.getLogger("rich")

def get_node_id(scope) -> int | None:
    try:
        query_string = parse_qs(scope["query_string"].decode("utf8"))
        return query_string.get("node_id", [None])[0]
    except Exception as e:
        log.error(f"Error getting node_id: {e}")
        return None

class ManagerConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Authentication is done in JWTAuthMiddleware
        if isinstance(self.scope["user"], AnonymousUser):
            log.debug("WEBSOCKET: Unauthorized.")
            await self.close()

        self.node_id = get_node_id(self.scope)
        await self.update_node_connection_status(self.node_id, "CONNECTED")
        await self.update_node_status(self.node_id, "PENDING")
        #await self.update_jobs_when_conn(self.node_id)
        await self.update_gpu_status(self.node_id, "PENDING")

        log.debug(f"WEBSOCKET: Node ID: {self.node_id}")
        if self.channel_layer:
            await self.channel_layer.group_add("nodes_group", self.channel_name)
            await self.accept()

    async def disconnect(self, _close_code):
        try:
            if hasattr(self, "node_id"):
                await self.update_node_connection_status(self.node_id, "DISCONNECTED")
                await self.update_node_status(self.node_id, "UNAVAILABLE")
                await self.update_gpu_status(self.node_id, "UNAVAILABLE")
                #await self.check_lost_connection(self.node_id)
                asyncio.create_task(self.check_lost_connection(self.node_id))
                asyncio.create_task(self.delayed_job_interruption(self.node_id, delay=60))

            if self.channel_layer:
                await self.channel_layer.group_discard("nodes_group", self.channel_name)
        except Exception as e:
            log.error(f"Disconnect session error: {e}")

    async def receive(self, text_data):
        msg = parse_message(text_data)
        if msg is None:
            return
        if msg.command == "register":
            await self.update_node_connection_status(msg.node_id, "CONNECTED")
        elif msg.command == "job_status":
            await self.handle_job_status(msg)

    @database_sync_to_async
    def handle_job_status(self, msg: WebsocketMessage):
        try:
            job = Job.objects.get(id=msg.job_id)
            job.status = msg.result["status"]
            job.output = msg.result.get("output")
            job.error = msg.result.get("error")
            job.end_time = msg.result.get("end_time")
            job.save()
        except Job.DoesNotExist:
            log.error(f"Job {msg.job_id} does not exisrt")

    @database_sync_to_async
    def update_node_connection_status_internal(self, node_id, status):
        try:
            node = Node.objects.get(id=node_id)
            node.status = status
            node.save()
        except Node.DoesNotExist:
            pass  # Handle the case where the node does not exist.

    async def delayed_job_interruption(self, node_id, delay):
        await asyncio.sleep(delay)
        await self.interrupt_long_disconnected_jobs(node_id)

    @database_sync_to_async
    def interrupt_long_disconnected_jobs(self, node_id):
        try:
            log.debug("STARTING INTERR WAIT")
            disconnected_time_threshold = timezone.now() - timezone.timedelta(minutes=30)
            log.debug(f"Disconnection threshold time: {disconnected_time_threshold}")

            jobs_to_interrupt = Job.objects.filter(
                node__id=node_id,
                node__connection_status="DISCONNECTED",
                node__last_seen__lt=disconnected_time_threshold,
                status="CONNECTION_LOST"
            )
            log.debug(f"Jobs to interrupt {jobs_to_interrupt}")

            for job in jobs_to_interrupt:
                log.debug(f"Interrupting job {job.id}")
                job.status = "INTERRUPTED"
                job.save()
        except Exception as e:
            log.error(f"Error interrupting jobs: {e}")

    @database_sync_to_async
    def check_lost_connection(self, node_id):
        try:
            disconnected_time_threshold = timezone.now() - timezone.timedelta(minutes=30)
            log.debug(f"Lost connection threshold time: {disconnected_time_threshold}")

            jobs_to_interrupt = Job.objects.filter(
                node__id=node_id,
                node__connection_status="DISCONNECTED",
                #node__last_seen__lt=disconnected_time_threshold,
                status="RUNNING"
            )
            log.debug(f"Jobs with lost connection: {jobs_to_interrupt}")

            for job in jobs_to_interrupt:
                log.debug(f"Marking job {job.id} as CONNECTION_LOST")
                job.status = "CONNECTION_LOST"
                job.save()
        except Exception as e:
            log.error(f"Error checking lost connection: {e}")

    @database_sync_to_async
    def update_node_connection_status(self, node_id: int, connection_status: str):
        log.debug(f"Updating node {node_id} status to {connection_status}")
        return Node.objects.filter(id=node_id).update(
            connection_status=connection_status
        )

    @database_sync_to_async
    def update_node_status(self, node_id: int, status: str):
        log.debug(f"Updating node {node_id} status to {status}")
        return Node.objects.filter(id=node_id).update(
            status=status
        )

    async def send_test_message(self, message):
        if self.channel_layer:
            await self.channel_layer.group_send(
                "nodes_group",
                {
                    "type": "send_message_to_group",
                    "message": message,
                },
            )

    @database_sync_to_async
    def update_jobs_when_conn(self, node_id):
        jobs_to_interrupt = Job.objects.filter(
            node__id=node_id,
            status="RUNNING"
        )
        for job in jobs_to_interrupt:
            log.debug(f"Interrupting job {job.id}")
            job.status = "INTERRUPTED"
            job.save()

    @database_sync_to_async
    def update_gpu_status(self, node_id, status):
        try:
            gpus = Gpu.objects.filter(node__id=node_id)
            for gpu in gpus:
                log.debug(f"Updating GPU {gpu.id} status to {status}")
                gpu.status = status
                gpu.save()
        except Gpu.DoesNotExist:
            pass

    async def send_message_to_group(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def websocket_message(self, event):
        """
        Handle messages sent to the group with type 'websocket.message'.
        This method name corresponds to the 'type' key in the message sent by send_message function.
        """
        try:
            msg = WebsocketMessage(**json.loads(event["text"]))
        except Exception as e:
            log.error(f"Error parsing message: {e}")
            return
        log.debug(f"WEBSOCKET: Sending message: {msg.model_dump_json()}")
        await self.send(text_data=msg.model_dump_json())
