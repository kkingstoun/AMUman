import asyncio
import logging
from dataclasses import asdict
from typing import Any, Dict

import httpx  # Użyj httpx dla asynchronicznych zapytań HTTP
from datetime import datetime, timezone

from .job import Job, JobStatus

log = logging.getLogger("rich")


class JobManager:
    def __init__(self, node_id: int, manager_url: str) -> None:
        self.node_id: int = node_id
        self.manager_url: str = manager_url

    async def run_job(self, job_id: int) -> None:
        self.job = await self.fetch_job_from_manager(job_id)
        self.async_task = asyncio.create_task(self.run_subprocess())

        # TODO: Check if interrupted
        # job.end_time = datetime.now().isoformat()
        # job.status = "Finished"

    async def post_updated_job_to_manager(self) -> None:
        url: str = f"http://{self.manager_url}/api/jobs/{self.job.id}/"
        async with httpx.AsyncClient() as client:
            try:
                log.debug(f"Sending updated job to `{url}`")
                response = await client.put(url, json=self.job.asdict)
                if response.status_code <= 400:
                    updated_job: Dict[str, Any] = response.json()
                    log.debug(f"Received updated job: {updated_job}")
                else:
                    log.error(f"Error sending updated job: Status code {response.status_code}")
            except Exception as e:
                log.exception(f"Error sending updated job to manager: {e}")

    async def fetch_job_from_manager(self, job_id: int) -> Job:
        url: str = f"http://{self.manager_url}/api/jobs/{job_id}/"
        job_data: Dict[
            str, Any
        ] = {}
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                job_data = response.json()
                log.debug(f"Received job: {job_data}")
            else:
                log.error(f"Error fetching job: Status code {response.status_code}")
        try:
            return Job(**job_data)

        except Exception as e:
            log.error(f"Error while casting the job API response to dataclass: {e}")
            raise e  # Consider how you want to handle this error, e.g., raise or return a default value

    async def run_subprocess(self) -> None:
        log.debug(f"job_starting subprocess for job ID: {self.job.id}")
        cmd = ["amumax", self.job.path]

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
                self.job.output=stdout.decode()
            if stderr:
                log.debug(f"[STDERR for job ID: {self.job.id}]\n{stderr.decode()}")
                self.error=stderr.decode()

            if self.subprocess.returncode == 0:
                self.job.status = JobStatus.FINISHED
                self.job.end_time=datetime.now().isoformat()
            else:
                self.job.status = JobStatus.INTERRUPTED
                self.job.error_time=datetime.now().isoformat()

            await self.post_updated_job_to_manager()

            log.info(f"Job started AMUmax for job ID: {self.job.id} (PID: {self.subprocess.pid})")
            log.info(f"AMUmax exited with status {self.job.status}.")

        except OSError as e:
            communicate = f"Failed to job_start subprocess for job ID: {self.job.id}. Executable may not be found. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED
            self.output = communicate
            await self.post_updated_job_to_manager()
        except ValueError as e:
            communicate = f"Invalid arguments provided to `create_subprocess_exec` for job ID: {self.job.id}. Arguments: {cmd}. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED
            self.output = communicate
            await self.post_updated_job_to_manager()

        except asyncio.CancelledError:
            log.info(f"Subprocess job_start was cancelled for job ID: {self.job.id}.")
        except Exception as e:
            communicate =  f"Unexpected error occurred while job_starting subprocess for job ID: {self.job.id}. Error: {e}"
            log.error(communicate)
            self.job.status = JobStatus.INTERRUPTED.value
            self.output = communicate
            await self.post_updated_job_to_manager()

    async def stop_process(self) -> None:
        if self.subprocess and self.subprocess.returncode is None:
            log.debug(f"Stopping amumax for job ID: {self.job.id}")
            self.subprocess.terminate()
            self.job.status = JobStatus.INTERRUPTED.value
            await self.post_updated_job_to_manager()


