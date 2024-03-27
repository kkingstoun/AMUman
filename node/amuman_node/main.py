import asyncio
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

from amuman_node.api import API
from amuman_node.gpu_monitor import GPUMonitor
from amuman_node.job_manager import JobRunner
from amuman_node.websockets import Websockets, parse_message

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
        self.api: API = API()
        self.node_id: int = int(os.getenv("NODE_ID", 0))
        self.node_name: str = os.getenv("NODE_NAME", str(uuid.uuid1()))
        self.node_user: str = os.getenv("NODE_USER", "admin")
        self.node_password: str = os.getenv("NODE_PASSWORD", "admin")
        log.debug(f"Node ID: {self.node_id}, Node Name: '{self.node_name}'")
        self.ws = Websockets(self.api, self.node_id, self.node_name)

        self.reconnect_attempts: int = 10
        self.reconnect_delay: int = 10
        self.gpm: Optional[GPUMonitor] = None
        self.access_token: str
        self.refresh_token: Optional[str] = None
        self.is_registered = False
        self.is_connected = False

        self.reply_timeout = 10
        self.ping_timeout = 5
        self.sleep_time = 5

    async def start(self) -> None:
        while True:
            try:
                if (
                    not self.is_registered or self.is_connected
                ) and self.register_with_manager():
                    await self.websocket_loop()
            except Exception as e:
                log.error(f"Cannot register to manager! {e}")
                await asyncio.sleep(self.sleep_time)

    def get_own_ip(self) -> str:
        try:
            ip: str = requests.get("https://api.ipify.org").content.decode("utf8")
            log.debug(f"IP={ip}")
            return ip
        except Exception as err:
            log.exception(f"Unable to get the external IP: {err}")
            return "error"

    def register_with_manager(self) -> bool:
        if not self.api.authenticate():
            return False
        data: dict[str, Any] = {
            "name": self.node_name,
            "ip": self.get_own_ip(),
            "number_of_gpus": 0,
        }
        log.debug(f"Registering data: {data=}")

        try:
            response = self.api.register(data)
            if response.status_code in [200, 201]:
                self.node_id = int(response.json().get("id"))
                log.debug(f"Node registered: {self.node_id=}")
                self.is_registered = True
                self.gpm = GPUMonitor(self.node_id, self.api)
                if response.status_code == 200:
                    self.gpm.api_post("update")
                elif response.status_code == 201:
                    self.gpm.api_post("assign")
                return True
            else:
                self.is_registered = False
                log.error(
                    f"Failed to register node. Status Code: {response.status_code}"
                )
                log.debug(response.text)

        except requests.exceptions.ConnectionError:
            log.error(f"Couldn't connect to the manager: {self.api.url}")
        except requests.exceptions.RequestException as e:
            log.exception(f"Error registering the node: {e}")
        return False

    async def websocket_loop(self) -> None:
        while True:
            log.debug("Creating new connection...")
            try:
                async with websockets.connect(
                    self.ws.url, extra_headers=self.api.headers
                ) as ws:
                    while True:
                        try:
                            await self.ws.register(ws)
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
                                    f"WEBSOCKET: Lost connection, retrying in {self.sleep_time}s"
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
                    await self.process_message(message)

            except websockets.ConnectionClosed:
                log.warning("Connection to the WebSocket server closed.")
                break

    async def process_message(self, message: str | bytearray | memoryview) -> None:
        if isinstance(message, str):
            msg = parse_message(message)
            if msg is None:
                return
            if msg.node_id != self.node_id:
                log.debug("Command not for this node.")
                return
            if msg.command == "update_gpus":
                log.info("Updating GPUs")
                await self.execute_update_gpus()
            elif msg.command == "run_job":
                if msg.job_id is None:
                    log.error("No job_id in message")
                    return
                log.info("Running job")
                JobRunner(self.node_id, self.api, msg.job_id)
            else:
                log.error(f"Unknown command: {msg.command}")

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
