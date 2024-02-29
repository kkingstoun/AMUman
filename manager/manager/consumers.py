import asyncio
import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from manager.models import Job, Node


class ManagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope['query_string'].decode('utf8'))
        self.node_id = query_string.get('node_id', [None])[0]  # Pobieranie wartości 'node_id'
        # Authentication should be done in JWTAuthMiddleware
        if self.scope["user"] is AnonymousUser:
            await self.close()
        else:
            await self.channel_layer.group_add("nodes_group", self.channel_name)
            await self.accept()

    async def disconnect(self, _close_code):
        if hasattr(self, 'node_id'):
            await self.update_node_status(self.node_id, 'DISCONNECTED')
        await self.channel_layer.group_discard("nodes_group", self.channel_name)
        asyncio.ensure_future(self.interrupt_long_DISCONNECTED_Jobs())

    @database_sync_to_async
    def update_node_status_internal(self, node_id, status):
        try:
            node = Node.objects.get(id=node_id)
            node.status = status
            node.save()
        except Node.DoesNotExist:
            pass  # Handle the case where the node does not exist.

    async def interrupt_long_DISCONNECTED_Jobs(self):
        while True:
            await asyncio.sleep(30 * 60)  # Wait for 30 minutes
            await self.check_and_interrupt_Jobs()

    @database_sync_to_async
    def check_and_interrupt_Jobs(self):
        DISCONNECTED_time_threshold = timezone.now() - timezone.timedelta(minutes=30)
        jobs_to_interrupt = Job.objects.filter(
            node__status='DISCONNECTED',
            node__last_seen__lt=DISCONNECTED_time_threshold,
            status='PENDING'
        )

        for job in jobs_to_interrupt:
            job.status = 'INTERRUPTED'
            job.save()


    @database_sync_to_async
    def update_node_status(self, node_id,  connection_status, name=None):
        if name is not None:
            return Node.objects.filter(id=node_id).update(
                name=name, connection_status=connection_status
            )
        else:
            return Node.objects.filter(id=node_id).update(
                connection_status=connection_status
            )

    async def receive(self, text_data):
        # Rozłóż wiadomość na dane
        data = json.loads(text_data)
        # print(data)
        if data.get("command", None) == "register":
            try:
                await self.update_node_status(
                    data["node_id"], "CONNECTED", data["node_name"]
                )
                await self.update_node_status(self.node_id, "CONNECTED")
                print("Registering node", data.get("node_name"))
                
            except Exception as e:
                print("Error", data.get("node_name"), str(e))
                await self.update_node_status(
                    data["node_id"], "DISCONNECTED", data["node_name"]
                )
        else:
            await self.send_test_message("test")
            await self.send(
                text_data=json.dumps(
                    {"message": "Hello I'm WS server. Nice to meet you."}
                )
            )
        # Wykonaj jakąś logikę w oparciu o dane
        if data["message"] == "Hello from Node!":
            # Wysłaj odpowiedź
            await self.send(text_data=json.dumps({"message": "Welcome, node!"}))

    async def send_test_message(self, message):
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

    async def node_command(self, event):
        # Logika do obsługi komunikatu typu 'node.command'
        print(f"Otrzymano komendę: {event}")
        # Tworzenie słownika odpowiedzi na podstawie otrzymanych danych
        response_message = {key: event[key] for key in event if key != "type"}
        # Wysyłanie odpowiedzi do klienta 'node'
        await self.send(text_data=json.dumps(response_message))
