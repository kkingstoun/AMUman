import asyncio
import logging
from datetime import datetime

from amuman_node.api import API

from .job import Job, JobStatus

log = logging.getLogger("rich")


class JobRunner:
    def __init__(self, node_id: int, api: API, job_id: int) -> None:
        self.node_id: int = node_id
        self.api: API = api
        self.subprocess: asyncio.subprocess.Process
        self.job: Job = self.api.get_job(job_id)
        self.async_task = asyncio.create_task(self.run_subprocess())

        # TODO: Check if interrupted
        # job.end_time = datetime.now().isoformat()
        # job.status = "Finished"

    async def run_subprocess(self) -> None:
        cmd: list[str] = ["amumax", "-gpu=1", "-magnets=false", self.job.path]
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
            # log.debug(f"[STDOUT for job ID: {self.job.id}]\n{stdout.decode()}")
            self.job.output = stdout.decode()
        if stderr:
            # log.debug(f"[STDERR for job ID: {self.job.id}]\n{stderr.decode()}")
            self.job.error = stderr.decode()

    async def _handle_completion(self) -> None:
        if self.subprocess.returncode == 0:
            self.job.status = JobStatus.FINISHED
        else:
            self.job.status = JobStatus.INTERRUPTED
            self.job.error_time = datetime.now().isoformat()
            log.debug(f"AMUmax exited with status {self.job.status.name}.")
        self.job.end_time = datetime.now().isoformat()
        try:
            res = self.api.update_job(self.job)
        except Exception as e:
            log.error(f"Failed to update job ID: {self.job.id}. Error: {e}")
            return
        log.debug(
            f"Job ID: {self.job.id}(completed) updated with status: {self.job.status.name}."
        )
        log.debug(f"Response: {res.json()}")

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
            res = self.api.update_job(self.job)
            log.debug(
                f"Job ID: {self.job.id}(error) updated with status: {self.job.status.name}. Response: {res.json()}"
            )

    async def stop_process(self) -> None:
        if self.subprocess and self.subprocess.returncode is None:
            log.debug(f"Stopping amumax for job ID: {self.job.id}")
            self.subprocess.terminate()
            self.job.status = JobStatus.INTERRUPTED
            self.api.update_job(self.job)
