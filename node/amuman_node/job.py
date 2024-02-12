import asyncio
import logging
from asyncio.subprocess import Process
from dataclasses import dataclass, field
from typing import Optional

log = logging.getLogger("rich")


@dataclass
class Job:
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
    subprocess: Optional[Process] = field(default=None)
    end_time: Optional[str] = field(default=None)
    error_time: Optional[str] = field(default=None)
    assigned_node_id: Optional[int] = field(default=None)
    assigned_gpu_id: Optional[int] = field(default=None)

    def start(self) -> None:
        log.debug(f"Starting job {self.id=}")
        self.async_task = asyncio.create_task(self.run_subprocess())

    async def run_subprocess(self) -> None:
        log.debug(f"Starting subprocess for job ID: {self.id}")
        cmd = ["amumax", self.path]

        try:
            self.subprocess = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            log.info(
                f"Subprocess started successfully for job ID: {self.id} (PID: {self.subprocess.pid})"
            )
        except OSError as e:
            log.error(
                f"Failed to start subprocess for job ID: {self.id}. Executable may not be found. Error: {e}"
            )
        except ValueError as e:
            log.error(
                f"Invalid arguments provided to `create_subprocess_exec` for job ID: {self.id}. Arguments: {cmd}. Error: {e}"
            )
        except asyncio.CancelledError:
            log.info(f"Subprocess start was cancelled for job ID: {self.id}.")
        except Exception as e:
            log.error(
                f"Unexpected error occurred while starting subprocess for job ID: {self.id}. Error: {e}"
            )

        log.info(f"Started amumax for job ID: {self.id} (PID: {self.subprocess.pid})")

        stdout, stderr = await self.subprocess.communicate()

        if stdout:
            log.debug(f"[STDOUT for job ID: {self.id}]\n{stdout.decode()}")
        if stderr:
            log.debug(f"[STDERR for job ID: {self.id}]\n{stderr.decode()}")

        log.debug(f"amumax exited with {self.subprocess.returncode}")

    def stop_process(self) -> None:
        if self.subprocess and self.subprocess.returncode is None:
            log.debug(f"Stopping amumax for job ID: {self.id}")
            self.subprocess.terminate()
