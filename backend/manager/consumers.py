# manager/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MasterConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.channel_layer.group_add("nodes_group", self.channel_name)
        await self.accept()
        # Wysyłanie testowej wiadomości po nawiązaniu połączenia

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("nodes_group", self.channel_name)

    async def receive(self, text_data):
        # Rozłóż wiadomość na dane
        data = json.loads(text_data)

        # Wykonaj jakąś logikę w oparciu o dane
        if data["message"] == "Hello from Node!":
            # Wysłaj odpowiedź
            await self.send(text_data=json.dumps({"message": "Witaj, node!"}))

    async def send_test_message(self, message):
        await self.channel_layer.group_send(
            "nodes_group",
            {
                "type": "send_message_to_group",
                "message": message,
            }
        )

    async def send_message_to_group(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    async def node_command(self, event):
        # Logika do obsługi komunikatu typu 'node.command'
        print(f"Otrzymano komendę: {event}")
        # Tworzenie słownika odpowiedzi na podstawie otrzymanych danych
        response_message = {key: event[key] for key in event if key != 'type'}
        # Wysyłanie odpowiedzi do klienta 'node'
        await self.send(text_data=json.dumps(response_message))