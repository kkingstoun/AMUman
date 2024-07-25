import json
import logging
import os
import string
import subprocess
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from enum import Enum
import requests

from amuman_node.api import API
from amuman_node.gpu import GPU, GPUStatus

log = logging.getLogger("rich")

class GPUMonitor:
    def __init__(self, node: int, api: API) -> None:
        self.node: int = node
        self.gpus: List[GPU] = self.get_gpus()
        self.api = api

    def get_gpus(self) -> List[GPU]:
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            gpu_count = len(output.strip().split("\n"))
        except subprocess.CalledProcessError as e:
            log.error(f"Failed to get GPU count: {e}")
            raise e

        return [GPU(device_id=id, node=self.node) for id in range(gpu_count)]

    def api_post(self, action: str) -> None:
        log.debug(f"GPU api post: {action}")
        action_word = "assigned" if action == "assign" else "updated"
        failure_action_word = "assign" if action == "assign" else "update"
        for gpu in self.gpus:
            if action == "update":
                print('update!!!!!!!')
                gpu.update_status()
            elif action == "bench":
                gpu.bench_speed()
            try:
                data = gpu.to_json()
                print(data)
                response = self.api.post_gpu(data)
                if response.status_code in [200, 201]:
                    log.info(
                        f"Successfully {action_word} GPU:{gpu.device_id} ({gpu.model}) to node {self.node}."
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
