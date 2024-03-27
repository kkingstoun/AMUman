import asyncio
import json
import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from manager.components.ws_messages import WebsocketMessage, parse_message
from manager.models import ConnectionStatus, Job, Node

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
        log.debug(f"WEBSOCKET: Node ID: {self.node_id}")
        if self.channel_layer:
            await self.channel_layer.group_add("nodes_group", self.channel_name)
            await self.accept()

    async def disconnect(self, _close_code):
        if hasattr(self, "node_id"):
            await self.update_node_status(self.node_id, "DISCONNECTED")
        if self.channel_layer:
            interrupt_task = asyncio.ensure_future(
                self.interrupt_long_disconnected_jobs()
            )
            await self.channel_layer.group_discard("nodes_group", self.channel_name)
            await interrupt_task

    async def receive(self, text_data):
        msg = parse_message(text_data)
        if msg is None:
            return
        if msg.command == "register":
            await self.update_node_status(msg.node_id, ConnectionStatus.CONNECTED)

    @database_sync_to_async
    def update_node_status_internal(self, node_id, status):
        try:
            node = Node.objects.get(id=node_id)
            node.status = status
            node.save()
        except Node.DoesNotExist:
            pass  # Handle the case where the node does not exist.

    async def interrupt_long_disconnected_jobs(self):
        while True:
            await asyncio.sleep(30 * 60)  # Wait for 30 minutes
            await self.check_and_interrupt_jobs()

    @database_sync_to_async
    def check_and_interrupt_jobs(self):
        disconnected_time_threshold = timezone.now() - timezone.timedelta(minutes=30)
        jobs_to_interrupt = Job.objects.filter(
            node__status="DISCONNECTED",
            node__last_seen__lt=disconnected_time_threshold,
            status="PENDING",
        )

        for job in jobs_to_interrupt:
            job.status = "INTERRUPTED"
            job.save()

    @database_sync_to_async
    def update_node_status(self, node_id: int, connection_status: ConnectionStatus):
        return Node.objects.filter(id=node_id).update(
            connection_status=connection_status
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
