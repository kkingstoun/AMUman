import asyncio
import logging
from datetime import datetime

from amuman_node.api import API

from .job import JobStatus

log = logging.getLogger("rich")


class JobManager:
    def __init__(self, node_id: int, api: API) -> None:
        self.node_id: int = node_id
        self.api = api

    async def run_job(self, job_id: int) -> None:
        self.job = self.api.get_job(job_id)
        self.async_task = asyncio.create_task(self.run_subprocess())

        # TODO: Check if interrupted
        # job.end_time = datetime.now().isoformat()
        # job.status = "Finished"

    async def run_subprocess(self) -> None:
        log.debug(f"job_starting subprocess for job ID: {self.job.id}")
        # TODO: Add support for choosing GPU
        cmd = ["amumax", "-gpu=1", "-magnets=false", self.job.path]
        log.debug(f"Running command: {cmd}")
        try:
            self.subprocess = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            log.info(
                f"Subprocess job_started successfully for job ID: {self.job.id} (PID: {self.subprocess.pid})"
            )
            stdout, stderr = await self.subprocess.communicate()
            if stdout:
                log.debug(f"[STDOUT for job ID: {self.job.id}]\n{stdout.decode()}")
                self.job.output = stdout.decode()
            if stderr:
                log.debug(f"[STDERR for job ID: {self.job.id}]\n{stderr.decode()}")
                self.job.error = stderr.decode()

            if self.subprocess.returncode == 0:
                self.job.status = JobStatus.FINISHED
                self.job.end_time = datetime.now().isoformat()
            else:
                self.job.status = JobStatus.INTERRUPTED
                self.job.error_time = datetime.now().isoformat()
                log.debug(f"AMUmax exited with status {self.job.status}.")

            self.api.update_job(self.job)

            log.info(
                f"Job started AMUmax for job ID: {self.job.id} (PID: {self.subprocess.pid})"
            )
            log.info(f"AMUmax exited with status {self.job.status}.")
            if self.job.output is not None:
                log.debug(f"AMUmax output: {self.job.output}")
            else:
                log.error(f"AMUmax error: {self.job.error}")

        except OSError as e:
            communicate = f"Failed to job_start subprocess for job ID: {self.job.id}. Executable may not be found. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED
            self.output = communicate
            self.api.update_job(self.job)

        except ValueError as e:
            communicate = f"Invalid arguments provided to `create_subprocess_exec` for job ID: {self.job.id}. Arguments: {cmd}. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED
            self.output = communicate
            self.api.update_job(self.job)

        except asyncio.CancelledError:
            log.info(f"Subprocess job_start was cancelled for job ID: {self.job.id}.")

        except Exception as e:
            communicate = f"Unexpected error occurred while job_starting subprocess for job ID: {self.job.id}. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED
            self.output = communicate
            self.api.update_job(self.job)

    async def stop_process(self) -> None:
        if self.subprocess and self.subprocess.returncode is None:
            log.debug(f"Stopping amumax for job ID: {self.job.id}")
            self.subprocess.terminate()
            self.job.status = JobStatus.INTERRUPTED
            self.api.update_job(self.job)
