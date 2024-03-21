import asyncio
import json
import logging
import os
import socket
import uuid
from typing import Any, Optional, Union

import requests
import websockets
from rich.logging import RichHandler
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedError,
    ConnectionClosedOK,
)

from amuman_node.gpu_monitor import GPUMonitor
from amuman_node.job_manager import JobManager

LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()

logging.basicConfig(
    level=LOGLEVEL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True, tracebacks_suppress=[websockets, requests])
    ],
)
log = logging.getLogger("rich")
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class NodeClient:
    def __init__(self) -> None:
        self.manager_url: str = os.getenv("MANAGER_URL", "localhost:8000")
        self.node_id: int = int(os.getenv("NODE_ID", 0))
        self.node_name: str = os.getenv("NODE_NAME", str(uuid.uuid1()))
        log.debug(
            f"Manager URL: '{self.manager_url}', Node ID: {self.node_id}, Node Name: '{self.node_name}'"
        )
        self.reconnect_attempts: int = 10
        self.reconnect_delay: int = 10
        self.gpm: Optional[GPUMonitor] = None
        self.access_token: str
        self.refresh_token: Optional[str] = None
        self.if_registred = False
        self.is_connected = False

        self.reply_timeout = 10
        self.ping_timeout = 5
        self.sleep_time = 5

    async def start(self) -> None:
        while True:
            try:
                if (
                    not self.if_registred or self.is_connected
                ) and self.register_with_manager():
                    await self.websocket_loop()
            except Exception as e:
                log.error(f"Cannot register to manager! {e}")
                await asyncio.sleep(self.sleep_time)

    def authenticate(self) -> bool:
        try:
            response = requests.post(
                f"http://{self.manager_url}/api/token/",
                json={
                    "username": os.getenv("NODE_USER", "admin"),
                    "password": os.getenv("NODE_PASSWORD", "admin"),
                },
            )
            log.debug(
                f"Authentication response: {response.status_code=}, {response.json()=}"
            )
        except requests.exceptions.RequestException as e:
            log.exception(f"Error authenticating the node: {e}")
            return False
        try:
            self.access_token = response.json()["access"]
            self.refresh_token = response.json()["refresh"]
            return True
        except (KeyError, TypeError):
            log.error("Unable to authenticate with the manager")
        return False

    def get_own_ip(self) -> str:
        try:
            ip: str = requests.get("https://api.ipify.org").content.decode("utf8")
            log.debug(f"IP={ip}")
            return ip
        except Exception as err:
            log.exception(f"Unable to get the external IP: {err}")
            return "error"

    def register_with_manager(self) -> bool:
        if not self.authenticate():
            return False
        data: dict[str, Any] = {
            "name": self.node_name,
            "ip": self.get_own_ip(),
            "number_of_gpus": 0,
        }
        log.debug(f"Registering data: {data=}")

        try:
            log.debug(data)
            log.debug(f"http://{self.manager_url}/api/nodes/")
            response = requests.post(
                f"http://{self.manager_url}/api/nodes/",
                json=data,
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            if response.status_code in [200, 201]:
                self.node_id = int(response.json().get("id"))
                log.debug(f"Node registered: {self.node_id=}")
                self.if_registred=True
                self.gpm = GPUMonitor(self.node_id, self.manager_url, self.access_token)
                if response.status_code == 200:
                    self.gpm.api_post("update")
                elif response.status_code == 201:
                    self.gpm.api_post("assign")
                return True
            else:
                self.if_registred = False
                log.error(
                    f"Failed to register node. Status Code: {response.status_code}"
                )
                log.debug(response.text)

        except requests.exceptions.ConnectionError:
            log.error(f"Couldn't connect to the manager ({self.manager_url})")
        except requests.exceptions.RequestException as e:
            log.exception(f"Error registering the node: {e}")
        return False

    async def register_websocket(self, ws: websockets.WebSocketClientProtocol) -> None:
        await ws.send(
            json.dumps(
                {
                    "command": "register",
                    "message": f"Hello from Node {self.node_name}!",
                    "node_id": self.node_id,
                    "node_name": self.node_name,
                }
            )
        )
        log.info("Websocket connection started.")

    async def websocket_loop(self) -> None:
        while True:
            log.debug("Creating new connection...")
            try:
                async with websockets.connect(
                    f"ws://{self.manager_url}/ws/node/?token={self.access_token}&node_id={self.node_id}"
                ) as ws:
                    while True:
                        try:
                            log.debug(
                                f"Registering with the manager: {self.manager_url}"
                            )
                            await self.register_websocket(ws)
                            log.debug(
                                f"Registered with the manager: {self.manager_url}"
                            )
                            await self.handle_connection(ws)
                        except (
                            asyncio.TimeoutError,
                            ConnectionClosed,
                            ConnectionClosedError,
                            ConnectionClosedOK,
                        ):
                            self.is_connected = False
                            self.is_registered = False
                            try:
                                pong = await ws.ping()
                                await asyncio.wait_for(pong, timeout=self.ping_timeout)
                                log.debug("Ping OK, keeping connection alive...")
                                continue
                            except Exception:
                                log.debug(
                                    f"Ping error - retrying connection in {self.sleep_time} sec (Ctrl-C to quit)"
                                )
                                await asyncio.sleep(self.sleep_time)
                                break
            except socket.gaierror:
                self.is_connected = False
                self.is_registered = False
                log.debug(
                    f"Socket error - retrying connection in {self.sleep_time} sec (Ctrl-C to quit)"
                )
                await asyncio.sleep(self.sleep_time)
                continue
            except ConnectionRefusedError:
                self.is_connected = False
                self.is_registered = False
                log.debug(
                    "Nobody seems to listen to this endpoint. Please check the URL."
                )
                log.debug(
                    f"Retrying connection in {self.sleep_time} sec (Ctrl-C to quit)"
                )
                await asyncio.sleep(self.sleep_time)
                continue

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
                    if isinstance(message, str):
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
                await self.execute_update_gpus()
            elif command == "run_job":
                log.info("Running job")
                self.job_manager: JobManager = JobManager(
                    self.node_id, self.manager_url, token=self.access_token
                )
                await self.job_manager.run_job(data["job_id"])
            else:
                log.error(f"Unknown command: {command}")
        elif command is not None:
            log.debug(
                f"Command not for this node: {command=}, {r_node_id=} != {self.node_id=}"
            )

    async def execute_update_gpus(self) -> None:
        if self.gpm and len(self.gpm.gpus) > 0:
            for gpu in self.gpm.gpus:
                log.debug(f"Updating GPU: {gpu.device_id}")
                gpu.update_status()
            self.gpm.api_post("update")


def entrypoint() -> None:
    try:
        asyncio.run(NodeClient().start())
    except KeyboardInterrupt:
        log.warning("Caught KeyboardInterrupt (Ctrl+C). Shutting down...")


if __name__ == "__main__":
    entrypoint()
