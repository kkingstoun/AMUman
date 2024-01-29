import asyncio
import websockets
import json
import logging
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from node.TaskManager import TaskManager

async def get_node_id():
    from node.models import Local
    local = await sync_to_async(get_object_or_404)(Local, pk=1)
    return int(local.node_id)
    
async def connect_to_manager():
    uri = "ws://localhost:8000/ws/node/"
    node_id = await get_node_id()
    tm = TaskManager(node_id)
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
                        print(message)
                        command = data.get("command")
                        r_node_id = data.get("node_id")
                        gpu_id = data.get("gpu_id",None)

                        if command == "update_gpus" and r_node_id == node_id:
                            await sync_to_async(execute_update_gpus)(node_id)
                        elif command is not None and r_node_id == node_id:
                            await tm.execute_command(command,data.get("task_id"))
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
