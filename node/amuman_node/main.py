import asyncio
import logging
import os
from typing import Any, Optional

import requests
import websockets
from rich.logging import RichHandler

from amuman_node.api import API
from amuman_node.config import Config
from amuman_node.gpu_monitor import GPUMonitor
from amuman_node.websockets import Websockets

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
logging.getLogger("asyncio").setLevel(logging.WARNING)


class NodeClient:
    def __init__(self) -> None:
        self.config: Config = Config()
        self.api: API = API(self.config)
        self.gpm: Optional[GPUMonitor] = None
        self.ws: Websockets

        self.run()

    def run(self) -> None:
        if self.register_with_manager():
            self.ws = Websockets(self.api, self.node_id, self.config.name, self.gpm)
            try:
                asyncio.run(self.ws.websocket_loop())
            except KeyboardInterrupt:
                log.warning("Caught KeyboardInterrupt (Ctrl+C). Shutting down...")
                # self.ws.close()

    def get_own_ip(self) -> str:
        try:
            ip: str = requests.get("https://api.ipify.org").content.decode("utf8")
            log.debug(f"IP={ip}")
            return ip
        except Exception as err:
            log.exception(f"Unable to get the external IP: {err}")
            return "error"

    def authenticate(self) -> bool:
        if not self.api.authenticate():
            log.error("Authentication failed")
            return False
        return True

    def register_with_manager(self) -> bool:
        if not self.api.authenticate():
            return False
        data: dict[str, Any] = {
            "name": self.config.name,
            "ip": self.get_own_ip(),
            "number_of_gpus": 0,  # ???
        }
        log.debug(f"Registering data: {data=}")

        try:
            response = self.api.post_node(data)
            if response.status_code in [200, 201]:
                self.node_id = int(response.json().get("id"))
                log.debug(f"Node registered: {self.node_id=}")
                self.gpm = GPUMonitor(self.node_id, self.api)
                if response.status_code == 200:
                    self.gpm.api_post("bench")
                    self.gpm.api_post("update")
                elif response.status_code == 201:
                    self.gpm.api_post("assign")
                return True
            else:
                log.error(
                    f"Failed to register node. Status Code: {response.status_code} {response.text}"
                )

        except requests.exceptions.ConnectionError:
            log.error(f"Couldn't connect to the manager: {self.api.url}")
        except requests.exceptions.RequestException as e:
            log.exception(f"Error registering the node: {e}")
        return False


def entrypoint() -> None:
    NodeClient()


if __name__ == "__main__":
    entrypoint()
