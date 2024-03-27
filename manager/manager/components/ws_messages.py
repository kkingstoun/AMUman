import json
import logging
from typing import Optional, Union

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pydantic import BaseModel

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


def send_message(msg: WebsocketMessage):
    # Serialize the Pydantic model to JSON string
    message_json = msg.model_dump_json()
    channel_layer = get_channel_layer()
    if channel_layer is None:
        log.error("Channel layer is not initialized.")
        return

    # Sending the message using group_send, including the 'type' key
    msg_dict = {
        "type": "websocket.message",
        "text": message_json,
    }
    async_to_sync(channel_layer.group_send)(
        "nodes_group",
        msg_dict,
    )
