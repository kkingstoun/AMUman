import asyncio
import websockets
import json

async def connect_to_manager():
    print("CONNECT")
    uri = "ws://localhost:8000/ws/node/"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({"message": "Hello from Node!"}))
            while True:
                try:
                    message = await websocket.recv()
                    print(f"Otrzymano wiadomość: {message}")
                except websockets.ConnectionClosed:
                    print("Połączenie z serwerem WebSocket zostało zamknięte.")
                    break  # Zakończ pętlę, jeśli połączenie jest zamknięte
    except Exception as e:
        print(f"Błąd połączenia WebSocket: {e}")

def start_client():
    print("asdasdas")
    asyncio.run(connect_to_manager())
