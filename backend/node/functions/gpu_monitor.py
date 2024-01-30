import subprocess
import time
from datetime import datetime
import requests
from django.core.management.base import BaseCommand
import os

class GPUMonitor(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(GPUMonitor, self).__init__(*args, **kwargs)
       
        self.node_id = os.environ['NODE_ID']
        self.NODE_MANAGEMENT_URL = f"http://{os.environ['MANAGER_URL']}/manager/node-management/"
        
        self.gpus = self.get_gpu_count()
        self.gpus_status = {
            i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)
        }
        self.number_of_gpus = len(self.gpus_status)

    def get_gpu_count(self):
        """Returns the number of available graphics cards."""
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            return len(output.strip().split("\n"))
        except subprocess.CalledProcessError:
            return 0

    def check_gpu_load(self, gpu_index=0, check_duration=2, threshold=20):
        start_time = time.time()
        gpu_util = 0
        while time.time() - start_time < check_duration:
            try:
                # Get load information for the specified GPU
                gpu_util, mem_util = map(
                    int,
                    subprocess.check_output(
                        [
                            "nvidia-smi",
                            "--query-gpu=utilization.gpu,utilization.memory",
                            "--format=csv,noheader,nounits",
                            "--id=" + str(gpu_index),
                        ]
                    )
                    .decode()
                    .strip()
                    .split(","),
                )

                # Return 'free' if the GPU is less loaded than the threshold
                if gpu_util < threshold and mem_util < threshold:
                    return "Waiting", gpu_util
            except subprocess.CalledProcessError as e:
                print(f"Error running nvidia-smi: {e}")
                return "error"
            except ValueError:
                print("Data conversion error.")
                return "error"
            time.sleep(1)  # Wait 1 second before the next check
        return 1, gpu_util

    def check_gpu_status(self, gpu_index=0):
        # Check the status of the specified GPU
        if gpu_index is not None and gpu_index != "":
            gpu_status, gpu_util = self.check_gpu_load(gpu_index=gpu_index)

            # Return a dictionary containing the status and utilization of the GPU
            return {
                "name": self.check_gpu_brand(gpu_index=gpu_index),
                "status": gpu_status,
                "gpu_util": gpu_util,
                "gpu_uuid": self.get_nvidia_gpu_uuid(gpu_index),
                "is_running_amumax": 1
                if self.check_for_amumax(gpu_index=gpu_index)
                else 0,
                "refresh_time": datetime.now().strftime("%d.%m.%Y, %H:%M:%S"),
            }
        else:
            return {i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)}

    def check_for_amumax(self, gpu_index=0):
        # Check if the process 'amumax' is running on the specified GPU
        try:
            output = subprocess.check_output(
                [
                    "nvidia-smi",
                    "-i",
                    str(gpu_index),
                    "--query-compute-apps=process_name",
                    "--format=csv,noheader",
                ]
            ).decode()
            processes = output.strip().split("\n")
            for process in processes:
                if process.strip().startswith("amumax"):
                    return True
            return False
        except subprocess.CalledProcessError as e:
            print(f"Subprocess error: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def check_gpu_brand(self, gpu_index=0):
        try:
            # The nvidia-smi command to read the model of the graphics card
            output = (
                subprocess.check_output(
                    [
                        "nvidia-smi",
                        "-i",
                        str(gpu_index),
                        "--query-gpu=gpu_name",
                        "--format=csv,noheader",
                    ]
                )
                .decode()
                .strip()
            )
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error running nvidia-smi: {e}")
            return None

    def get_nvidia_gpu_uuid(self, pk=0):
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            lines = output.strip().split("\n")
            uuids = [line.split("(")[-1].split(")")[0] for line in lines]
            if pk is not None:
                return uuids[pk]
            return uuids
        except Exception as e:
            print(f"Error getting GPU UUIDs: {e}")
            return None

    def assign_gpus(self, node_id):
        self.gpu_status = {
            i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)
        }
        for gpu_key, gpu in self.gpus_status.items():
            data = {
                "action": "assign_node_gpu",
                "no": gpu_key,
                "brand_name": gpu["name"],
                "gpu_util": gpu["gpu_util"],
                "status": gpu["status"],
                "node_id": node_id,
                "is_running_amumax": gpu["is_running_amumax"],
                "gpu_uuid": gpu["gpu_uuid"],
                "gpu_info": None,
            }

            try:
                response = requests.post(f"http://{os.environ['MANAGER_URL']}/manager/node-management/", data=data)
                if response.status_code == 200:
                    response_data = response.json()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfull new gpu {gpu_key} assign.")
                    )
                elif response.status_code == 201:
                    response_data = response.json()
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfull update of gpu {gpu_key}.")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error !!: {response.text}, Status Code: {response.status_code}"
                        )
                    )
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error2: {e}"))

    def submit_update_gpu_status(self,node_id):
        self.gpu_status = {
            i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)
        }
        for gpu_key, gpu in self.gpus_status.items():
            data = {
                "action": "update_node_gpu_status",
                "brand_name": gpu["name"],
                "gpu_util": gpu["gpu_util"],
                "status": gpu["status"],
                "node_id": self.node_id,
                "is_running_amumax": gpu["is_running_amumax"],
                "gpu_uuid": gpu["gpu_uuid"],
            }

            try:
                # import json
                # print(json.dumps(data))
                response = requests.post(f"http://{os.environ['NODE_MANAGEMENT_URL']}/manager/node-management/", data=data)
                if response.status_code == 200:
                    self.stdout.write(
                        self.style.SUCCESS(f"Successfull gpu {gpu_key} update.")
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Error !!: {response.text}, Status Code: {response.status_code}"
                        )
                    )
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error2: {e}"))
