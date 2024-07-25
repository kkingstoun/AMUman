import asyncio
import logging
import os
from datetime import datetime
from pathlib import Path

import requests
from requests.exceptions import ConnectionError

from amuman_node.api import API
from amuman_node.gpu_monitor import GPU, GPUMonitor, GPUStatus

#from .gpu_monitor import 
from .job import Job, JobStatus
from .node import Node, NodeStatus

log = logging.getLogger("rich")

SHARED_FOLDER = Path(os.environ.get("SHARED_FOLDER", "/shared"))

class JobRunner:
    def __init__(self, node_id: int, api: API, job_id: int, gpu_device_id: int, gpm: GPUMonitor) -> None:
        self.node_id: int = node_id
        self.api: API = api
        self.subprocess: asyncio.subprocess.Process
        self.job: Job = self.api.get_job(job_id)
        self.gpu_id = self.job.gpu
        self.gpu_device_id = gpu_device_id
        self.gpm: GPUMonitor = gpm
        self.async_task = None
        self.node: Node = self.api.get_node(node_id)
        self.gpu: GPU = self.api.get_gpu(self.gpu_id)[0]
        self.gpu_id: GPU = self.api.get_gpu(self.gpu_id)[1]


    async def run_job(self) -> None:
        self.async_task = asyncio.create_task(self.run_subprocess())

    async def run_subprocess(self) -> None:
        cmd: list[str] = [
            "amumax",
            f"-gpu={self.gpu_device_id}",
            "-magnets=false",
            str(SHARED_FOLDER / Path(self.job.path)),
        ]
        log.debug(f"Starting subprocess for job ID: {self.job.id} with command: {cmd}")

        try:
            await self._start_subprocess(cmd)
            await self._process_output()
            await self._handle_completion()
        except asyncio.CancelledError:
            log.info(f"Subprocess start was cancelled for job ID: {self.job.id}.")
        except (OSError, ValueError, Exception) as e:
            await self._handle_error(e)

    async def _start_subprocess(self, cmd: list[str]) -> None:
        self.subprocess = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        log.info(
            f"Subprocess started successfully for job ID: {self.job.id} (PID: {self.subprocess.pid})"
        )

    async def _process_output(self) -> None:
        stdout, stderr = await self.subprocess.communicate()
        if stdout:
            self.job.output = stdout.decode()
        if stderr:
            self.job.error = stderr.decode()

    async def _handle_completion(self) -> None:

        if self.subprocess.returncode == 0:
            self.job.status = JobStatus.FINISHED
            log.debug(f"?????????????????????????????????????????????????????????????")
            self.job.run_attempts += 1
            await self._update_job()
            self.node.status = NodeStatus.PENDING.value
            self.api.put_node(self.node)
            self.gpu.status = GPUStatus.PENDING.value
            self.gpu_json = self.gpu.to_json()
            self.api.put_gpu(self.gpu_json, self.gpu_id)

        else:

            log.debug(f"1 :-)))))))))")
            self.job.status = JobStatus.CALC_ERROR.value
            await self._update_job()
            log.debug(f"2 :-)))))))))")
            self.node.status = NodeStatus.PENDING.value
            self.api.put_node(self.node)
            
            self.gpu.status = GPUStatus.PENDING.value
        
            self.gpu_json = self.gpu.to_json()
            log.debug(f" :-(( {self.gpu_json, self.gpu_id}")
            self.api.put_gpu(self.gpu_json, self.gpu_id)
            log.debug(f"3 :-)))))))))")
          
            self.job.error_time = datetime.now().isoformat()
            self.job.run_attempts += 1
            log.debug(f"4 :-)))))))))")
            if self.job.run_attempts > 2:
              log.debug(f":-((((((((((((")
              #log.debug(f"???????? {self.job.id}")
              self.job.status = JobStatus.FAILED.value
              await self._update_job()
        
              self.gpu.status = GPUStatus.PENDING.value
              self.gpu_json = self.gpu.to_json()
              self.api.put_gpu(self.gpu_json, self.gpu_id)
              self.node.status = NodeStatus.PENDING
              self.api.put_node(self.node)
              return
  
            log.debug(f"AMUmax exited with status {self.job.status}.")
            await self._update_job()
        self.job.end_time = datetime.now().isoformat()
        #await self._update_job()

    async def _handle_error(self, error: Exception) -> None:
        error_message: str = ""
        if isinstance(error, OSError):
            error_message = f"Failed to start subprocess. Executable may not be found. Error: {error}"
        elif isinstance(error, ValueError):
            error_message = f"Invalid arguments provided to `create_subprocess_exec`. Error: {error}"
        elif isinstance(error, asyncio.CancelledError):
            log.info(f"Subprocess start was cancelled for job ID: {self.job.id}.")
            return
        else:
            error_message = f"Unexpected error occurred. Error: {error}"

        if error_message:
            log.error(error_message)
            self.job.status = JobStatus.INTERRUPTED
            self.job.error = error_message
            await self._update_job()

    async def _update_job(self) -> None:
        #attempts = 0
        #success = False
        #while attempts < 4 and not success:
            try:
                res = self.api.put_job(self.job)
                if res.status_code not in [200, 201]:
                    log.error(
                        f"Failed to update job ID: {self.job.id}, status code: {res.status_code}, response: {res.json()}"
                    )
                    return
                #success = True
            except ConnectionError as e:
                log.error(f"Failed to update job ID: {self.job.id}, connection error: {e}")
                await asyncio.sleep(5)
                #attempts += 1
                await self._update_job()
            except Exception as e:
                log.error(f"Failed to update job ID: {self.job.id}, error: {e}")
                await asyncio.sleep(5)
                await self._update_job()
                #attempts += 1

    async def stop_process(self) -> None:
        if self.subprocess and self.subprocess.returncode is None:
            log.debug(f"Stopping amumax for job ID: {self.job.id}")
            self.subprocess.terminate()
            self.job.status = JobStatus.INTERRUPTED
            await self._update_job()

    def is_running(self) -> bool:
        return self.async_task is not None and not self.async_task.done()

    def get_status(self) -> dict:
        return {
            "job_id": self.job.id,
            "status": self.job.status.name,
            "output": self.job.output,
            "error": self.job.error,
            "start_time": self.job.start_time,
            "end_time": self.job.end_time,
        }
