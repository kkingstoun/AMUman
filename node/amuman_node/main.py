import asyncio
import json
import logging
import os
import re
import uuid

# import dotenv
import websockets
from asgiref.sync import sync_to_async

from .gpu_monitor import GPUMonitor
from .task_manager import TaskManager


class NodeClient:
    def __init__(self):
        self.manager_url = (
            os.getenv("MANAGER_URL")
            if os.getenv("MANAGER_URL") not in [None, ""]
            else "localhost:8000"
        )
        self.node_id = (
            os.getenv("NODE_ID") if os.getenv("NODE_ID") not in [None, ""] else "0"
        )
        self.node_name = (
            os.getenv("NODE_NAME")
            if os.getenv("NODE_NAME") not in [None, ""]
            else str(uuid.uuid1())
        )
        print(self.manager_url, self.node_id, self.node_name)

        self.task_manager = TaskManager(self.node_id)
        self.reconnect_attempts = 10
        self.sleep_increment = 1

    @staticmethod
    def extract_integer_from_string(s):
        match = re.search(r"\d+", s)
        return int(match.group()) if match else None

    async def connect_to_manager(self):
        ws_url = f"ws://{self.manager_url}/ws/node"
        print(ws_url)
        while True:
            try:
                async with websockets.connect(ws_url) as websocket:
                    await self.handle_connection(websocket)
            except Exception as e:
                logging.error(f"WebSocket connection error: {e}")

            # Reconnection logic
            logging.info("Attempting to reconnect...")
            await self.reconnect()

    async def handle_connection(self, websocket):
        if self.node_id is not None:
            await websocket.send(
                json.dumps(
                    {
                        "command": "register",
                        "message": "Hello from Node!",
                        "node_id": self.node_id,
                        "node_name": self.node_name,
                    }
                )
            )
        print(
            f'\033[92mNode "{self.node_name}" connected to the Manager WebSocket.\033[0m'
        )
        self.gpm = GPUMonitor()
        while True:
            try:
                message = await websocket.recv()
                await self.process_message(message)
            except websockets.ConnectionClosed:
                logging.warning("Connection to the WebSocket server closed.")
                break

    async def process_message(self, message):
        data = json.loads(message)
        command = data.get("command")
        print(message)
        r_node_id = data.get("node_id")
        # r_gpu_id = data.get("gpu_id")
        print(r_node_id)
        if (self.node_id is None or self.node_id == 0) and r_node_id is not None:
            print("\033[92m Received node_id. Saving in .env file. \033[0m")
        if command == "update_gpus" and str(r_node_id) == str(self.node_id):
            await self.execute_update_gpus(self.node_id)
        elif command is not None and str(r_node_id) == str(self.node_id):
            await self.task_manager.execute_command(command, data.get("task_id"))
        elif command is not None:
            print(f"\033[92m {command} \033[0m")
            print(f"It's not my job: {str(r_node_id)} != {str(self.node_id)}")

    async def reconnect(self):
        for i in range(self.reconnect_attempts, 0, -1):
            logging.info(f"Reconnecting in {i}...")
            await asyncio.sleep(self.sleep_increment)

    async def execute_update_gpus(self, node_id):
        if self.gpm.number_of_gpus > 0:
            await sync_to_async(self.gpm.check_gpus_status)()
            await sync_to_async(self.gpm.submit_update_gpu_status)(node_id)


def entrypoint() -> None:
    client = NodeClient()
    asyncio.run(client.connect_to_manager())
