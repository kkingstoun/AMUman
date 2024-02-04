import asyncio
import logging
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
    end_time: Optional[str] = field(default=None)
    error_time: Optional[str] = field(default=None)
    assigned_node_id: Optional[int] = field(default=None)
    assigned_gpu_id: Optional[int] = field(default=None)

    def start(self):
        log.debug(f"Starting job {self.id=}")
        self.subprocess_task: Optional[asyncio.Task] = asyncio.create_task(
            self.run_subprocess()
        )

    async def run_subprocess(self) -> None:
        log.debug(f"Starting subprocess for {self.task.id=}")
        try:
            self.process = await asyncio.create_subprocess_exec(
                "amumax",
                self.task.path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except Exception as e:
            log.exception(e)
            return

        log.info(f"Started amumax (PID: {self.process.pid})")

        stdout, stderr = await self.process.communicate()

        if stdout:
            log.debug(f"[STDOUT]\n{stdout.decode()}")
        if stderr:
            log.debug(f"[STDERR]\n{stderr.decode()}")

        log.debug(f"amumax exited with {self.process.returncode}")

    def stop_process(self) -> None:
        if self.process:
            log.debug("Stopping amumax")
            self.process.terminate()  # Gracefully terminate the process
