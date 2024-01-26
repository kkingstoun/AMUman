# node/ws_client.py

import asyncio
import websockets
import json

async def connect_to_manager():
    print("dziala")
    uri = "ws://localhost:8000/ws/node/"  # Adres serwera WebSocket
    # async with websockets.connect(uri) as websocket:
    #     # Możesz tutaj wysłać jakieś dane lub po prostu nasłuchiwać
    #     await websocket.send(json.dumps({"message": "Hello from Node!"}))
    #     while True:
    #         message = await websocket.recv()
    #         print(f"Otrzymano wiadomość: {message}")
            
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            # Zakładamy, że wiadomości są w formacie JSON
            print(message)
            data = json.loads(message)
            if "command" in data:
                handle_command(data["command"])

def handle_command(command):
    print(f"Otrzymano polecenie: {command}")
    # Tu możesz dodać logikę do obsługi różnych poleceń
    
asyncio.get_event_loop().run_until_complete(connect_to_manager())
