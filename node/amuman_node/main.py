import asyncio
import json
import logging
import os
import uuid
from typing import Any, Optional, Union

import requests
import websockets
from rich.logging import RichHandler

from .gpu_monitor import GPUMonitor
from .job_manager import JobManager

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


class NodeClient:
    def __init__(self) -> None:
        self.manager_url: str = os.getenv("MANAGER_URL", "localhost:8000")
        self.node_id: int = int(os.getenv("NODE_ID", 0))
        self.node_name: str = os.getenv("NODE_NAME", str(uuid.uuid1()))
        log.debug(
            f"Manager URL: '{self.manager_url}', Node ID: {self.node_id}, Node Name: '{self.node_name}'"
        )

        self.job_manager: JobManager = JobManager(self.node_id, self.manager_url)
        self.reconnect_attempts: int = 10
        self.reconnect_delay: int = 30
        self.gpm: Optional[GPUMonitor] = None

    async def start(self) -> None:
        self.register_with_manager()
        await self.connect_to_manager()

    def get_own_ip(self) -> str:
        try:
            ip: str = requests.get("https://api.ipify.org").content.decode("utf8")
            log.debug(f"IP={ip}")
            return ip
        except Exception as err:
            log.exception(f"Unable to get the external IP: {err}")
            return "error"

    def register_with_manager(self) -> None:
        data: dict[str, Any] = {
            "action": "assign_new_node",
            "node_name": self.node_name,
            "ip": self.get_own_ip(),
            "port": None,
            "number_of_gpus": 0,
        }
        log.debug(f"Registering data: {data=}")

        try:
            response = requests.post(
                f"http://{self.manager_url}/manager/node-management/", json=data
            )
            if response.status_code in [200, 201]:
                self.node_id = int(response.json().get("id"))
                log.debug(f"Node registered: {self.node_id=}")
                self.gpm = GPUMonitor(self.node_id, self.manager_url)

                if response.status_code == 200:
                    self.gpm.api_post("assign")
                # 201 = exists and modified ?
                elif response.status_code == 201:
                    self.gpm.api_post("update")
        except requests.exceptions.RequestException as e:
            log.exception(f"Error registering the node: {e}")

    async def register_websocket(self, ws: websockets.WebSocketClientProtocol) -> None:
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

    async def connect_to_manager(self) -> None:
        while True:
            try:
                async with websockets.connect(
                    f"ws://{self.manager_url}/ws/node"
                ) as websocket:
                    self.reconnect_attemps = 10
                    await self.register_websocket(websocket)
                    await self.handle_connection(websocket)
            except Exception as e:
                log.exception(f"WebSocket connection error: {e}")

            if self.reconnect_attempts > 0:
                log.warning(f"{self.reconnect_attemps} reconnection attempts left")
                log.warning(f"Reconnecting in {self.reconnect_delay} seconds...")
                await asyncio.sleep(self.reconnect_delay)
                self.reconnect_attemps -= 1

    async def handle_connection(
        self, websocket: websockets.WebSocketClientProtocol
    ) -> None:
        while True:
            try:
                message: Union[str, bytes] = await websocket.recv()
                if isinstance(message, bytes):
                    log.error("Received bytes instead of plain text from websocket")
                else:
                    log.debug(f"Received message: {message}")
                    await self.process_message(message)
            except websockets.ConnectionClosed:
                log.warning("Connection to the WebSocket server closed.")
                break

    async def process_message(self, message: str) -> None:
        data: dict[str, Any] = json.loads(message)
        command: Optional[str] = data.get("command")
        r_node_id: Optional[int] = data.get("node_id")
        log.debug(f"{r_node_id=}, {self.node_id=}")

        if str(r_node_id) == str(self.node_id):
            if command == "update_gpus":
                log.info("Updating GPUs")
                await self.execute_update_gpus(self.node_id)
            elif command == "run_task":
                log.info("Running job")
                await self.job_manager.run_job(data["task_id"])
            else:
                log.error(f"Unknown command: {command}")
        elif command is not None:
            log.debug(
                f"Command not for this node: {command=}, {r_node_id=} != {self.node_id=}"
            )

    async def execute_update_gpus(self, node_id: int) -> None:
        if self.gpm and len(self.gpm.gpus) > 0:
            await self.gpm.check_gpus_status()
            await self.gpm.submit_update_gpu_status(node_id)


def entrypoint() -> None:
    try:
        asyncio.run(NodeClient().start())
    except KeyboardInterrupt:
        log.warning("Caught KeyboardInterrupt (Ctrl+C). Shutting down...")
