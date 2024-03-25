import json
import logging

import websockets

from amuman_node.api import API

log = logging.getLogger("rich")


class Websockets:
    def __init__(self, api: API, node_id: int, node_name: str) -> None:
        self.api: API = api
        self.node_name: str = node_name
        self.node_id: int = node_id
        self.url = f"{self.api.url.replace('http','ws').replace('/api','')}/ws/node/?token={self.api.access_token}&node_id={self.node_id}"

    async def register(self, ws: websockets.WebSocketClientProtocol) -> None:
        log.info("WEBSOCKET: Registering with the manager...")
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
        log.info("WEBSOCKET: Connection started.")
