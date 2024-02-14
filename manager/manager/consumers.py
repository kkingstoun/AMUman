import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from manager.models import Node


class ManagerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("nodes_group", self.channel_name)
        await self.accept()
        # Wysyłanie testowej wiadomości po nawiązaniu połączenia

    async def disconnect(self, _close_code):
        await self.channel_layer.group_discard("nodes_group", self.channel_name)

    @database_sync_to_async
    def update_node_status(self, node_id, name, connection_status):
        return Node.objects.filter(id=node_id).update(
            name=name, connection_status=connection_status
        )

    async def receive(self, text_data):
        # Rozłóż wiadomość na dane
        data = json.loads(text_data)
        # print(data)
        if data.get("command", None) == "register":
            try:
                await self.update_node_status(
                    data["node_id"], data["node_name"], "Connected"
                )
                print("Registering node", data.get("node_name"))
            except Exception as e:
                print("Error", data.get("node_name"), str(e))
                await self.update_node_status(
                    data["node_id"], data["node_name"], "Disconnected"
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
