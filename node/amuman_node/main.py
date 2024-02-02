import asyncio
import json
import logging
import os
import uuid

import requests

# import dotenv
import websockets
from asgiref.sync import sync_to_async
from rich.logging import RichHandler

from .gpu_monitor import GPUMonitor
from .task_manager import TaskManager

logging.basicConfig(
    level="DEBUG",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True, tracebacks_suppress=[websockets, requests])
    ],
)
log = logging.getLogger("rich")
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
log.debug("*" * 60)
log.debug("*" * 60)


class NodeClient:
    def __init__(self):
        self.manager_url = (
            os.getenv("MANAGER_URL")
            if os.getenv("MANAGER_URL") not in [None, ""]
            else "localhost:8000"
        )
        self.node_id = int(
            os.getenv("NODE_ID") if os.getenv("NODE_ID") not in [None, ""] else 0
        )
        self.node_name = (
            os.getenv("NODE_NAME")
            if os.getenv("NODE_NAME") not in [None, ""]
            else str(uuid.uuid1())
        )
        log.debug(f"{self.manager_url=}, {self.node_id=}, {self.node_name=}")

        self.task_manager = TaskManager(self.node_id, self.manager_url)
        self.reconnect_attempts = 10
        self.sleep_increment = 1

    async def start(self):
        self.register_with_manager()
        await self.connect_to_manager()

    def get_own_ip(self):
        try:
            ip = requests.get("https://api.ipify.org").content.decode("utf8")
            log.debug(f"{ip=}")
            return ip
        except Exception as err:
            log.exception(f"Unable to get the external IP: {err}")
            return EOFError

    def register_with_manager(self):
        data = {
            "action": "assign_new_node",
            "node_name": self.node_name,
            "ip": self.get_own_ip(),
            "port": None,
            "number_of_gpus": 0,
        }
        log.debug(f": {data=}")

        try:
            response = requests.post(
                f"http://{self.manager_url}/manager/node-management/",
                data=data,
            )
            if response.status_code in [200, 201]:
                self.node_id = int(response.json().get("id"))
                log.debug(f"Node registered: {self.node_id=}")
                self.gpm = GPUMonitor(self.node_id, self.manager_url)

            if response.status_code == 200:
                self.gpm.assign_gpus(self.node_id)

            # 201: Success + update
            elif response.status_code == 201:
                self.gpm.submit_update_gpu_status(self.node_id)

        except requests.exceptions.RequestException as e:
            log.exception(f"Error registering the node: {e}")

    async def register_websocket(self, ws):
        await ws.send(
            json.dumps(
                {
                    "command": "register",
                    "message": "Hello from Node!",
                    "node_id": self.node_id,
                    "node_name": self.node_name,
                }
            )
        )
        log.info("Websocket connection started.")

    async def connect_to_manager(self):
        while True:
            try:
                async with websockets.connect(
                    f"ws://{self.manager_url}/ws/node"
                ) as websocket:
                    await self.register_websocket(websocket)
                    await self.handle_connection(websocket)
            except Exception as e:
                log.exception(f"WebSocket connection error: {e}")

            log.info("Attempting to reconnect...")
            await self.reconnect()

    async def handle_connection(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                log.debug(f"Received message :{message}")
                await self.process_message(message)
            except websockets.ConnectionClosed:
                log.warning("Connection to the WebSocket server closed.")
                break

    async def process_message(self, message):
        data = json.loads(message)
        command = data.get("command")
        r_node_id = data.get("node_id")
        log.debug(f"{r_node_id=}, {self.node_id=}")

        if str(r_node_id) == str(self.node_id):
            if command == "update_gpus":
                log.info("Updating gpus")
                await self.execute_update_gpus(self.node_id)
            elif command == "run_task":
                log.info("Running task")
                await self.task_manager.run_task(data["task_id"])
            else:
                log.error(f"Command unknown: {command}")
        elif command is not None:
            log.debug(f"Command not for me: {command=},{r_node_id=} != {self.node_id=}")

    async def reconnect(self):
        for i in range(self.reconnect_attempts, 0, -1):
            log.info(f"Reconnecting in {i}...")
            await asyncio.sleep(self.sleep_increment)

    async def execute_update_gpus(self, node_id):
        if self.gpm.number_of_gpus > 0:
            await sync_to_async(self.gpm.check_gpus_status)()
            await sync_to_async(self.gpm.submit_update_gpu_status)(node_id)


def entrypoint() -> None:
    try:
        asyncio.run(NodeClient().start())
    except KeyboardInterrupt:
        log.warning("Caught KeyboardInterrupt (Ctrl+C). Shutting down...")
