import json
import logging
from typing import Optional, Union

import websockets
from pydantic import BaseModel

from amuman_node.api import API

log = logging.getLogger("rich")


class WebsocketMessage(BaseModel):
    command: str
    node_id: int
    job_id: Optional[int] = None
    gpu_device_id: Optional[int] = None


def parse_message(message: str) -> Union[WebsocketMessage, None]:
    try:
        data = json.loads(message)
        return WebsocketMessage(**data)
    except ValueError as e:
        log.error(f"Error parsing message: {e}")
        return None


class Websockets:
    def __init__(self, api: API, node_id: int, node_name: str) -> None:
        self.api: API = api
        self.node_name: str = node_name
        self.node_id: int = node_id
        self.url = f"{self.api.url.replace('http','ws').replace('/api','')}/ws/node/?node_id={self.node_id}"

    async def register(self, ws: websockets.WebSocketClientProtocol) -> None:
        log.info("WEBSOCKET: Registering with the manager...")
        await ws.send(
            WebsocketMessage(command="register", node_id=self.node_id).model_dump_json()
        )
        log.info("WEBSOCKET: Connection started.")
