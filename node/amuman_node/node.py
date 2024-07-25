import asyncio
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, Optional
from datetime import datetime

log = logging.getLogger("rich")

class ConnectionStatus(Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"

class NodeStatus(Enum):
    PENDING = "PENDING"
    RESERVED = "RESERVED"
    UNAVAILABLE = "UNAVAILABLE"

@dataclass
class Node:
    id: int
    ip: str
    name: str
    number_of_gpus: int
    status: NodeStatus = NodeStatus.PENDING
    connection_status: ConnectionStatus = ConnectionStatus.CONNECTED
    last_seen: datetime = field(default_factory=datetime.now)

    def asdict(self) -> Dict[str, str]:
        result = asdict(self)
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value
        return result

    def __str__(self):
        return f"{self.id}"
