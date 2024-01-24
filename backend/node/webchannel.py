import json
from channels.generic.websocket import AsyncWebsocketConsumer

class WebChannel(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']

        # Tutaj możesz przetwarzać otrzymane dane i wysyłać odpowiedzi do Node
        await self.send(text_data=json.dumps({'message': 'Odpowiedź od serwera'}))
