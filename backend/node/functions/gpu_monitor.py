import subprocess
import time
from datetime import datetime

class GPUMonitor:

    def __init__(self):
        self.gpus = self.get_gpu_count()
        self.gpus_status = {i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)}

    def get_gpu_count(self):
        """Returns the number of available graphics cards."""
        try:
            output = subprocess.check_output(["nvidia-smi", "-L"]).decode()
            return len(output.strip().split("\n"))
        except subprocess.CalledProcessError:
            return 0

    def check_gpu_load(self, gpu_index=0, check_duration=2, threshold=20):
        start_time = time.time()
        while time.time() - start_time < check_duration:
            try:
                # Get load information for the specified GPU
                gpu_util, mem_util = map(int, subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu,utilization.memory", "--format=csv,noheader,nounits", "--id=" + str(gpu_index)]).decode().strip().split(","))

                # Return 'free' if the GPU is less loaded than the threshold
                if gpu_util < threshold and mem_util < threshold:
                    return 0, gpu_util
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
                "is_running_amumax": 1 if self.check_for_amumax(gpu_index=gpu_index) else 0,
                "refresh_time": datetime.now().strftime("%d.%m.%Y, %H:%M:%S")
            }
        else:
            return {i: self.check_gpu_status(gpu_index=i) for i in range(self.gpus)}

    def check_for_amumax(self, gpu_index=0):
        # Check if the process 'amumax' is running on the specified GPU
        try:
            output = subprocess.check_output(["nvidia-smi", "-i", str(gpu_index), "--query-compute-apps=process_name", "--format=csv,noheader"]).decode()
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
            output = subprocess.check_output(["nvidia-smi", "-i", str(gpu_index), "--query-gpu=gpu_name", "--format=csv,noheader"]).decode().strip()
            return output
        except subprocess.CalledProcessError as e:
            print(f"Error running nvidia-smi: {e}")
            return None



# gpm = GPUMonitor()
# # print(gpm.check_for_amumax2(0))
# # print(gpm.check_gpu_load(gpu_index=1))

# gpm.check_gpu_status(index=0)