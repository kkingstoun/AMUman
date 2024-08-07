import json
import logging
import os
import string
import subprocess
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List,Dict
from enum import Enum
import requests

log = logging.getLogger("rich")

class GPUStatus(Enum):
    RUNNING = "RUNNING"
    PENDING = "PENDING"
    RESERVED = "RESERVED"  # not implemented
    UNAVAILABLE = "UNAVAILABLE"  # High usage not from job or error

@dataclass
class GPU:
    device_id: int
    node: int
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
    speed_score: str = field(default=0.0)  

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
        # self.speed = self.get_gpu_performance_category()
        self.is_running_amumax = self.check_is_amumax_running()
        self.refresh_time = datetime.now()

    def bench_speed(self) -> None:
        log.info("Benching GPUs")
        self.amumax_run()


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

    def get_gpu_load_status(self, threshold: int = 90) -> str:
        if self.check_is_amumax_running() is True:
            return "RUNNING"
        else:
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
        #log.debug("AMUMAX CHECK")
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
            "NVIDIA GeForce RTX 2060": "FAST",
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
            "NVIDIA GeForce RTX 4080 SUPER": "FAST",
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
    
    def amumax_run(self) -> float:
        self.command = ["amumax", "-magnets=0", "/app/node/amuman_node/bench.mx3"]
        try:
            result = subprocess.run(self.command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=False)
            log.debug(f"Amumax benchmark: {result} ")
            return self.read_zattrs('/app/node/amuman_node/bench.zarr')
           
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to run amumax benchmark: {e}")
            raise e
            
    def read_zattrs(self, path_zarr) -> string:
        path_zattrs = os.path.join(path_zarr, '.zattrs')
        if os.path.exists(path_zattrs):
            try:
                with open(path_zattrs, 'r') as file:
                    data_zattrs = json.load(file)
                    total_time = float((data_zattrs['total_time'])[:-1])
                    self.speed_score = total_time
                    self.speed = self.switch(total_time)
                    return(self.speed)
            except ValueError:
                log.error("Decoding JSON file has failed")    
                
    def switch(self, time):
        if time < 30:
            return "FAST"
        elif 30 <= time < 60:
            return "STANDARD"        
        elif time >= 60:
            return "SLOW"               
    
    def to_json(self):
        data = {
            "device_id": self.device_id,
            "node": self.node,
            "model": self.model,
            "uuid": self.uuid,
            "util": self.gpu_util,
            "is_running_amumax": self.is_running_amumax,
            "status": self.status,
            "speed": self.speed,
            "speed_score": self.speed_score,
            "last_update": self.refresh_time.strftime("%Y-%m-%d %H:%M:%S"),
            #"last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data
    
    def asdict(self) -> Dict[str, str]:
        result = asdict(self)
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value
        return result

    def __str__(self):
        return f"{self.id}"