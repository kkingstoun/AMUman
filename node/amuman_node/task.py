from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    id: int
    user: str
    path: str
    node_name: str
    port: int
    submit_time: str
    start_time: str
    priority: str
    gpu_partition: str
    est: int
    status: str
    output: str
    error: str
    flags: str
    end_time: Optional[str] = field(default=None)
    error_time: Optional[str] = field(default=None)
    assigned_node_id: Optional[int] = field(default=None)
    assigned_gpu_id: Optional[int] = field(default=None)
