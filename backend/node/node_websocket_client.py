import asyncio
import websockets
import json
from asgiref.sync import sync_to_async

async def get_node_id():
    from node.models import Local
    from asgiref.sync import sync_to_async
    node_id = await sync_to_async(Local.objects.get, thread_sensitive=True)(id=1)
    return node_id.id
    
async def connect_to_manager():
    uri = "ws://manager:8000/ws/node/"
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                # Send initial message after connection
                await websocket.send(json.dumps({"message": "Hello from Node!"}))

                # Main loop to receive and handle messages
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        command = data.get("command")
                        r_node_id = data.get("node_id")
                        node_id = await get_node_id()

                        if command == "update_gpus" and r_node_id == node_id:
                            await sync_to_async(execute_update_gpus)(node_id)
                        else:
                            pass  # Placeholder for other commands

                    except websockets.ConnectionClosed:
                        logging.warning("Connection to the WebSocket server closed.")
                        break

        except Exception as e:
            logging.error(f"WebSocket connection error: {e}")

        # Reconnection logic
        logging.info("Attempting to reconnect...")
        for i in range(10, 0, -1):
            logging.info(f"Reconnecting in {i}...")
            await asyncio.sleep(1)
            
def execute_update_gpus(node_id):
    from node.functions.gpu_monitor import GPUMonitor
    GPUMonitor().submit_update_gpu_status(node_id)
    
def start_client():
    asyncio.run(connect_to_manager())
