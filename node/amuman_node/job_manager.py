import logging
from dataclasses import asdict
from datetime import datetime
from typing import Any, Dict

import requests

from .job import Job

log = logging.getLogger("rich")


class JobManager:
    def __init__(self, node_id: int, manager_url: str) -> None:
        self.node_id: int = node_id
        self.manager_url: str = manager_url

    async def run_job(self, job_id: int) -> None:
        job: Job = await self.fetch_job_from_manager(job_id)

        job.status = "Running"
        job.start_time = datetime.now().isoformat()
        await self.post_updated_job_to_manager(job)
        log.debug(f"Starting the job: {job.id=}")
        # Run the job without blocking the main thread
        job.start()

        # TODO: Check if interrupted
        job.end_time = datetime.now().isoformat()
        job.status = "Finished"

    async def post_updated_job_to_manager(self, job: Job) -> None:
        url: str = f"http://{self.manager_url}/api/tasks/{job.id}/"

        data: Dict[str, Any] = asdict(job)
        try:
            log.debug(f"Sending updated job to `{url}`")
            response: requests.Response = requests.put(url, json=data)
            if response.status_code <= 400:
                updated_job: Dict[str, Any] = response.json()
                log.debug(f"Received updated job: {updated_job}")
            elif response.status_code >= 400:
                log.error(
                    f"Error sending updated job: Status code {response.status_code}"
                )
        except Exception as e:
            log.exception(f"Error sending updated job to manager: {e}")

    async def fetch_job_from_manager(self, job_id: int) -> Job:
        url: str = f"http://{self.manager_url}/api/tasks/{job_id}/"
        job_data: Dict[
            str, Any
        ] = {}  # Initialize job_data to prevent reference before assignment
        try:
            log.debug(f"Fetching job from `{url}`")
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                job_data = response.json()
                log.debug(f"Received job: {job_data}")
            else:
                log.error(f"Error fetching job: Status code {response.status_code}")
                # Consider raising an exception or returning None if the job cannot be fetched
        except Exception as e:
            log.error(f"Error fetching job from manager: {e}")
            # Consider raising an exception or returning None if the job cannot be fetched

        # Create and return a Job instance from job_data
        try:
            job: Job = Job(**job_data)
            return job
        except Exception as e:
            log.error(f"Error while casting the job API response to dataclass: {e}")
            raise e  # Consider how you want to handle this error, e.g., raise or return a default value
