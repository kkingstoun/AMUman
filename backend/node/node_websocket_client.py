import asyncio
import json
import logging
import os
import re
import time
import websockets
import dotenv
from asgiref.sync import sync_to_async
from node.TaskManager import TaskManager
from os import system

class NodeClient:
    def __init__(self):
        self.dotenv_file = "/app/.env"
        dotenv.load_dotenv(self.dotenv_file)
        system("cat /app/.env")
        print("print:", self.dotenv_file)
        
        self.manager_url = dotenv.get_key(self.dotenv_file, "MANAGER_URL")
        
        print(self.manager_url)
        
        self.node_id = self.extract_integer_from_string(
            dotenv.get_key(self.dotenv_file, "NODE_ID")
        )
        
        self.task_manager = TaskManager(self.node_id)
        self.reconnect_attempts = 10
        self.sleep_increment = 1

    @staticmethod
    def extract_integer_from_string(s):
        match = re.search(r"\d+", s)
        return int(match.group()) if match else None

    def generate_system_key(self):
        return dotenv.get_key(self.dotenv_file, "NODE_NAME")

    async def connect_to_manager(self):
        wsl_url = f"ws://{self.manager_url}/ws/node"
        while True:
            try:
                async with websockets.connect(wsl_url) as websocket:
                    await self.handle_connection(websocket)
            except Exception as e:
                logging.error(f"WebSocket connection error: {e}")

            # Reconnection logic
            logging.info("Attempting to reconnect...")
            await self.reconnect()

    async def handle_connection(self, websocket):
        await websocket.send(
            json.dumps(
                {"message": "Hello from Node!", "node_key": self.generate_system_key()}
            )
        )
        print(
            f'\033[92mNode "{self.generate_system_key()}" connected to the Manager WebSocket.\033[0m'
        )
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
        r_node_id = data.get("node_id")
        if self.node_id is None and r_node_id is not None:
            print(f"\033[92m Received node_id. Saving in .env file. \033[0m")
            dotenv.set_key(self.dotenv_file, "NODE_ID", r_node_id)
        if command == "update_gpus" and str(r_node_id) == str(self.node_id):
            await sync_to_async(self.execute_update_gpus)(self.node_id)
        elif command is not None and str(r_node_id) == str(self.node_id):
            await self.task_manager.execute_command(command, data.get("task_id"))
        elif command is not None:
            print(f"\033[92m {command} \033[0m")
            print(f"It's not my job: {str(r_node_id)} != {str(self.node_id)}")

    async def reconnect(self):
        for i in range(self.reconnect_attempts, 0, -1):
            logging.info(f"Reconnecting in {i}...")
            await asyncio.sleep(self.sleep_increment)

    @staticmethod
    def execute_update_gpus(node_id):
        from node.functions.gpu_monitor import GPUMonitor

        GPUMonitor().submit_update_gpu_status(node_id)


def start_client():
    client = NodeClient()
    asyncio.run(client.connect_to_manager())

