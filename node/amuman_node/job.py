import asyncio
import json
import logging
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional

log = logging.getLogger("rich")

class JobPriority(Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"

class JobStatus(Enum):
    WAITING = "Waiting"
    PENDING = "Pending"
    RUNNING = "Running"
    FINISHED = "Finished"
    INTERRUPTED = "Interrupted"

class GPUPartition(Enum):
    SLOW = "Slow"
    NORMAL = "Normal"
    FAST = "Fast"

@dataclass
class Job:
    id: int
    path: str
    user: str
    node: int
    gpu: int
    user: str
    port: Optional[int] = None
    submit_time: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_time: Optional[str] = None
    priority: JobPriority = JobPriority.NORMAL
    gpu_partition: GPUPartition = GPUPartition.NORMAL
    duration: int = 1
    status: JobStatus = JobStatus.WAITING
    output: Optional[str] = None
    error: Optional[str] = None
    flags: Optional[str] = None
    subprocess: Optional[asyncio.subprocess.Process] = field(default=None)

    @property
    def asdict(self):
        result = asdict(self)
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value  # Zamień Enum na wartość tekstową
        return result
