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

    async def run_task(self, task_id: int) -> None:
        job: Job = await self.fetch_task_from_manager(task_id)

        job.status = "Running"
        job.start_time = datetime.now().isoformat()
        await self.post_updated_job_to_manager(job)
        log.debug(f"Starting the job: {job.id=}")
        self.job = await job.start()

        # TODO: Check if interrupted
        job.end_time = datetime.now().isoformat()
        job.status = "Finished"

    async def post_updated_task_to_manager(self, task: Job) -> None:
        url: str = f"http://{self.manager_url}/manager/api/tasks/{task.id}/"

        data: Dict[str, Any] = asdict(task)
        try:
            log.debug(f"Sending updated task to `{url}`")
            response: requests.Response = requests.put(url, json=data)
            if response.status_code == 200:
                updated_task: Dict[str, Any] = response.json()
                log.debug(f"Received updated task: {updated_task}")
            else:
                log.exception(
                    f"Error sending updated task: Status code {response.status_code}"
                )
        except Exception as e:
            log.exception(f"Error sending updated task to manager: {e}")

    async def fetch_task_from_manager(self, task_id: int) -> Job:
        url: str = f"http://{self.manager_url}/manager/api/tasks/{task_id}/"
        task_data: Dict[
            str, Any
        ] = {}  # Initialize task_data to prevent reference before assignment
        try:
            log.debug(f"Fetching task from `{url}`")
            response: requests.Response = requests.get(url)
            if response.status_code == 200:
                task_data = response.json()
                log.debug(f"Received task: {task_data}")
            else:
                log.error(f"Error fetching task: Status code {response.status_code}")
                # Consider raising an exception or returning None if the task cannot be fetched
        except Exception as e:
            log.error(f"Error fetching task from manager: {e}")
            # Consider raising an exception or returning None if the task cannot be fetched

        # Create and return a Job instance from task_data
        try:
            task: Job = Job(**task_data)
            return task
        except Exception as e:
            log.error(f"Error while casting the task API response to dataclass: {e}")
            raise e  # Consider how you want to handle this error, e.g., raise or return a default value
