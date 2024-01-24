# node/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Tutaj obsłuż przychodzące wiadomości
        pass
