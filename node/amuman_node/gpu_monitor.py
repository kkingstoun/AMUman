import logging
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

import requests

log = logging.getLogger("rich")


@dataclass
class GPU:
    device_id: int
    node_id: int
    model: str = field(default="Unknown")  # Renamed from name to model
    uuid: str = field(default="")
    gpu_util: int = field(default=0)
    mem_util: int = field(default=0)
    status: str = field(default="PENDING")  # Use default value from GPUStatus
    is_running_amumax: bool = field(default=False)
    refresh_time: datetime = field(
        default_factory=lambda: datetime.now()
    )  # Use default_factory
    speed: str = field(default="NORMAL")  # Add speed field

    # Do we want it to run when the GPU class is created?
    def __post_init__(self) -> None:
        self.update_status()

    def update_status(self) -> None:
        log.info(f"GPU {self.device_id} updating status")
        self.model = self.get_model()
        self.uuid = self.get_uuid()
        self.gpu_util = self.get_gpu_util()
        self.mem_util = self.get_mem_util()
        self.status = self.get_gpu_load_status()
        self.speed = self.get_gpu_performance_category()
        self.is_running_amumax = self.check_is_amumax_running()
        self.refresh_time = datetime.now()

    def query_nvidia_smi(self, query: str) -> str:
        try:
            output = (
                subprocess.check_output(
                    [
                        "nvidia-smi",
                        "-i",
                        str(self.device_id),
                        query,
                        "--format=csv,noheader,nounits",
                    ]
                )
                .decode()
                .strip()
            )
            return output
        except subprocess.CalledProcessError as e:
            log.error(f"Error running nvidia-smi for GPU {self.device_id}: {e}")
        except Exception as e:
            log.error(f"Unexpected error for GPU {self.device_id}: {e}")
        return ""

    def get_gpu_load_status(self, threshold: int = 30) -> str:
        if self.gpu_util < threshold and self.mem_util < threshold:
            status = "PENDING"
        else:
            status = "UNAVAILABLE"
        log.debug(f"GPU {self.device_id} status: {status}")
        return status

    def get_gpu_util(self) -> int:
        gpu_util = int(self.query_nvidia_smi("--query-gpu=utilization.gpu"))
        log.debug(f"GPU {self.device_id} utilization: {gpu_util}%")
        return gpu_util

    def get_mem_util(self) -> int:
        mem_util = int(self.query_nvidia_smi("--query-gpu=utilization.memory"))
        log.debug(f"GPU {self.device_id} memory utilization: {mem_util}%")
        return mem_util

    def check_is_amumax_running(self) -> bool:
        output = self.query_nvidia_smi("--query-compute-apps=process_name")
        is_running = "amumax" in output if output else False
        log.debug(f"GPU {self.device_id} amumax running: {is_running}")
        return is_running

    def get_model(self) -> str:
        model = self.query_nvidia_smi("--query-gpu=gpu_name")
        log.debug(f"GPU {self.device_id} model: {model}")
        return model

    def get_gpu_performance_category(self) -> str:
        gpu_performance = {
            "NVIDIA GeForce GTX 960": "SLOW",
            "NVIDIA GeForce GTX 970": "SLOW",
            "NVIDIA GeForce GTX 980": "SLOW",
            "NVIDIA GeForce GTX 980 Ti": "SLOW",
            "NVIDIA GeForce GTX 1050": "SLOW",
            "NVIDIA GeForce GTX 1050 Ti": "SLOW",
            "NVIDIA GeForce GTX 1060": "NORMAL",
            "NVIDIA GeForce GTX 1070": "NORMAL",
            "NVIDIA GeForce GTX 1070 Ti": "NORMAL",
            "NVIDIA GeForce GTX 1080": "NORMAL",
            "NVIDIA GeForce GTX 1080 Ti": "NORMAL",
            "NVIDIA GeForce GTX 1650": "SLOW",
            "NVIDIA GeForce GTX 1650 SUPER": "NORMAL",
            "NVIDIA GeForce GTX 1660": "NORMAL",
            "NVIDIA GeForce GTX 1660 SUPER": "NORMAL",
            "NVIDIA GeForce GTX 1660 Ti": "NORMAL",
            "NVIDIA GeForce RTX 2060": "NORMAL",
            "NVIDIA GeForce RTX 2060 SUPER": "NORMAL",
            "NVIDIA GeForce RTX 2070": "NORMAL",
            "NVIDIA GeForce RTX 2070 SUPER": "FAST",
            "NVIDIA GeForce RTX 2080": "FAST",
            "NVIDIA GeForce RTX 2080 SUPER": "FAST",
            "NVIDIA GeForce RTX 2080 Ti": "FAST",
            "NVIDIA GeForce RTX 3060": "NORMAL",
            "NVIDIA GeForce RTX 3060 Ti": "FAST",
            "NVIDIA GeForce RTX 3070": "FAST",
            "NVIDIA GeForce RTX 3070 Ti": "FAST",
            "NVIDIA GeForce RTX 3080": "FAST",
            "NVIDIA GeForce RTX 3080 Ti": "FAST",
            "NVIDIA GeForce RTX 3090": "FAST",
            "NVIDIA GeForce RTX 3090 Ti": "FAST",
            "NVIDIA GeForce RTX 4070": "FAST",
            "NVIDIA GeForce RTX 4070 Ti": "FAST",
            "NVIDIA GeForce RTX 4080": "FAST",
            "NVIDIA GeForce RTX 4090": "FAST",
            # Dodaj tutaj dodatkowe modele zgodnie z potrzebą.
        }
        return gpu_performance.get(self.model, "Unknown")

    def get_uuid(self) -> str:
        raw_uuid = self.query_nvidia_smi("--query-gpu=uuid")
        # Usuń prefiks "GPU-" z UUID
        uuid = raw_uuid.replace("GPU-", "").strip()
        log.debug(f"GPU {self.device_id} UUID: {uuid}")
        return uuid

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "device_id": self.device_id,
            "node": self.node_id,
            "model": self.model,
            "uuid": self.uuid,
            "util": self.gpu_util,
            "is_running_amumax": self.is_running_amumax,
            "status": self.status,
            "speed": self.speed,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data


class GPUMonitor:
    def __init__(self, node_id: int, manager_url: str) -> None:
        self.node_id: int = node_id
        self.manager_url: str = manager_url
        self.gpus: List[GPU] = self.get_gpus()

    def get_gpus(self) -> List[GPU]:
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            gpu_count = len(output.strip().split("\n"))
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get GPU count: {e}")
            raise e

        return [GPU(device_id=id, node_id=self.node_id) for id in range(gpu_count)]

    def api_post(self, action: str) -> None:
        log.debug(f"GPU api post: {action}")
        action_word = "assigned" if action == "assign" else "updated"
        failure_action_word = "assign" if action == "assign" else "update"
        for gpu in self.gpus:
            if action == "update":
                gpu.update_status()
            try:
                data = gpu.to_dict()
                log.debug(f"Sending {data}")
                response = requests.post(
                    f"http://{self.manager_url}/api/gpus/",
                    json=data,
                )
                if response.status_code in [200, 201]:
                    log.info(
                        f"Successfully {action_word} GPU:{gpu.device_id} ({gpu.model}) to node {self.node_id}."
                    )
                else:
                    error_message = (
                        f"Failed to {failure_action_word} GPU:{gpu.device_id} ({gpu.model}). "
                        f"Server responded with status code: {response.status_code}."
                    )
                    if response.status_code == 500:
                        try:
                            error_details = (
                                response.json()
                            )  # Assuming the server error response is in JSON format
                            error_message += f" Error details: {error_details}"
                        except ValueError:
                            # If response is not in JSON format, fallback to logging the text content
                            error_message += " Error content was not json"
                    log.error(error_message)
            except requests.exceptions.RequestException as e:
                log.exception(f"Network error during GPU {failure_action_word}: {e}")
