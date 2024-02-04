import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

import requests

log = logging.getLogger("rich")


@dataclass
class GPU:
    id: int
    node_id: int
    name: str = field(init=False)
    uuid: str = field(init=False)
    gpu_util: int = field(init=False)
    mem_util: int = field(init=False)
    status: str = field(init=False)
    is_running_amumax: bool = field(init=False)
    refresh_time: str = field(init=False)

    def __post_init__(self) -> None:
        self.update_status()

    def update_status(self) -> None:
        log.debug(f"Updating status for GPU {self.id}")
        self.name = self.get_name()
        self.uuid = self.get_uuid()
        self.gpu_util = self.get_gpu_util()
        self.mem_util = self.get_mem_util()
        self.status = self.get_gpu_load_status()
        self.is_running_amumax = self.check_is_amumax_running()
        self.refresh_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def query_nvidia_smi(self, query: str) -> str:
        try:
            output = (
                subprocess.check_output(
                    [
                        "nvidia-smi",
                        "-i",
                        str(self.id),
                        query,
                        "--format=csv,noheader,nounits",
                    ]
                )
                .decode()
                .strip()
            )
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Error running nvidia-smi for GPU {self.id}: {e}")
        except Exception as e:
            log.error(f"Unexpected error for GPU {self.id}: {e}")
        return ""

    def get_gpu_load_status(self, check_duration: int = 2, threshold: int = 20) -> str:
        log.debug(f"Checking load status for GPU {self.id}")
        if self.gpu_util < threshold and self.mem_util < threshold:
            return "Waiting"
        else:
            return "Busy"

    def get_gpu_util(self) -> int:
        gpu_util = int(self.query_nvidia_smi("--query-gpu=utilization.gpu"))
        log.debug(f"GPU {self.id} utilization: {gpu_util}%")
        return gpu_util

    def get_mem_util(self) -> int:
        mem_util = int(self.query_nvidia_smi("--query-gpu=utilization.memory"))
        log.debug(f"GPU {self.id} memory utilization: {mem_util}%")
        return mem_util

    def check_is_amumax_running(self) -> bool:
        output = self.query_nvidia_smi("--query-compute-apps=process_name")
        is_running = "amumax" in output if output else False
        log.debug(f"Amumax running on GPU {self.id}: {is_running}")
        return is_running

    def get_name(self) -> str:
        name = self.query_nvidia_smi("--query-gpu=gpu_name")
        log.debug(f"GPU {self.id} name: {name}")
        return name

    def get_uuid(self) -> str:
        uuid = self.query_nvidia_smi("--query-gpu=uuid")
        log.debug(f"GPU {self.id} UUID: {uuid}")
        return uuid

    def to_dict(self) -> Dict[str, str]:
        data = {
            "action": "assign_node_gpu",
            "node_id": str(self.node_id),
            "brand_name": str(self.name),
            "gpu_util": str(self.gpu_util),
            "status": str(self.status),
            "is_running_amumax": str(self.is_running_amumax),
            "gpu_uuid": str(self.uuid),
            "gpu_info": "",
        }

        log.debug(f"GPU {self.id} to_dict: {data}")
        return data


class GPUMonitor:
    def __init__(self, node_id: int, manager_url: str) -> None:
        self.node_id: int = node_id
        self.manager_url: str = manager_url
        self.node_management_url: str = (
            f"http://{self.manager_url}/manager/node-management/"
        )
        self.gpus: List[GPU] = self.get_gpus()

    def get_gpus(self) -> List[GPU]:
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            gpu_count = len(output.strip().split("\n"))
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get GPU count: {e}")
            raise e

        return [GPU(id=id, node_id=self.node_id) for id in range(gpu_count)]

    def post_assign_gpus(self) -> None:
        """Assign GPUs to a node."""
        # Clean up once the API is decent
        for gpu in self.gpus:
            try:
                response = requests.post(self.node_management_url, json=gpu.to_dict())
                if response.status_code in [200, 201]:
                    log.info(
                        f"Successfully assigned GPU:{gpu.id} ({gpu.name}) to node {self.node_id}."
                    )
                else:
                    log.error(
                        f"Failed to assign GPU:{gpu.id} ({gpu.name}). Server responded with status code: {response.status_code}."
                    )
            except requests.exceptions.RequestException as e:
                log.exception(f"Network error during GPU assignment: {e}")

    def post_update_node_gpu_status(self) -> None:
        """Update the status of GPUs."""
        # Clean up once the API is decent
        for gpu in self.gpus:
            gpu.update_status()
            try:
                response = requests.post(self.node_management_url, json=gpu.to_dict())
                if response.status_code == 200:
                    log.info(
                        f"Successfully updated status for GPU:{gpu.id} ({gpu.name}) on node {self.node_id}."
                    )
                else:
                    log.error(
                        f"Failed to update status for GPU:{gpu.id} ({gpu.name}). Server responded with status code: {response.status_code}."
                    )
            except requests.exceptions.RequestException as e:
                log.exception(f"Network error during GPU status update: {e}")
        else:
            log.error("Node ID is None. Cannot update GPU status.")
