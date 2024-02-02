import logging
from dataclasses import asdict
from datetime import datetime

import requests

from .job_processs import JobProcess
from .task import Task

log = logging.getLogger("rich")


class TaskManager:
    def __init__(self, node_id: int, manager_url: str):
        self.node_id = node_id
        self.manager_url = manager_url

    async def run_task(self, task_id):
        task = await self.fetch_task_from_manager(task_id)
        log.debug(f"Starting the task: {task}")
        job_process = JobProcess(task)

        task.status = "Running"
        task.start_time: datetime.now().isoformat()
        await self.post_updated_task_to_manager(task)
        self.task = await job_process.run_subprocess()

        # TODO: Check if interupted
        task.end_time: datetime.now().isoformat()
        task.status = "Finished"

    async def post_updated_task_to_manager(self, task):
        url = f"http://{self.manager_url}/manager/api/tasks/{task.id}/"

        data = asdict(task)
        try:
            log.debug(f"Sending updated task to `{url}`")
            response = requests.put(url, json=data)
            if response.status_code == 200:
                updated_task = response.json()
                log.debug(f"Received updated task: {updated_task}")
            else:
                log.exception(
                    f"Error sending updated task: Status code {response.status_code}"
                )
        except Exception as e:
            log.exception(f"Error sending updated task to manager {e}")

    async def fetch_task_from_manager(self, task_id):
        url = f"http://{self.manager_url}/manager/api/tasks/{task_id}/"
        try:
            log.debug(f"Fetching task from `{url}`")
            response = requests.get(url)
            if response.status_code == 200:
                task_data = response.json()
                log.debug(f"Received task: {task_data}")
            else:
                log.error(f"Error fetching task: Status code {response.status_code}")
        except Exception as e:
            log.error(f"Error fetching task from manager {e}")

        try:
            task = Task(**task_data)
        except Exception as e:
            log.error(f"Error while casting the task api response to dataclass: {e}")

        return task
