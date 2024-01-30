import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
from common_models.models import * # Załóżmy, że te modele są zdefiniowane w aplikacji
import asyncio
import signal
import requests
import httpx
from datetime import datetime
import json
from subprocess import PIPE
import logging
logger = logging.getLogger(__name__)

class JobProcess:
    def __init__(self, task: Task):
        self.process = None
        self.task = task

    def remove_none(self,variable):
        return [x for x in variable if x is not None]

    async def run_subprocess(self):
        try:
            print(f"Path: {self.task.path}")
            # print(f"Flags: {self.flags}")
            if not self.task.path:
                raise ValueError("Ścieżka do amumax jest pusta")

            # flags = self.flags or []  # Handle the case when self.flags is None
            flags = ["-gpu", self.task.assigned_gpu_id]  # Add GPU id to flags
            args = self.remove_none(["amumax", *flags, self.task.path])

            print(args)
            
            self.process = await asyncio.create_subprocess_exec(
                *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            logger.info(f"Started amumax (PID: {self.process.pid})")
            self.task = await self.monitor_process(self.process)
            
            await asyncio.to_thread(self.task.save)
            return self.task

        except Exception as e:
            print(f"Error in running subprocess: {e}")
            await self.update_task_status(-1, None, str(e), self.task)


    async def monitor_process(self, process):
        while True:
            if process.returncode is not None:
                print("Process finished")
                stdout, stderr = await process.communicate()
                print(stdout,stderr)
                return await self.update_task_status(process.returncode, stdout, stderr, self.task)
            else:
                await asyncio.sleep(0.1)  # Check process status every 0.1 seconds
        return self.task
    async def update_task_status(self, return_code, stdout, stderr, task):
        task = await asyncio.to_thread(Task.objects.get, id=self.task.id)
        task.status = 'Finished' if return_code == 0 else 'Error'
        task.output = stdout.decode() if stdout else ''
        task.error = stderr.decode() if stderr else ''
        await asyncio.to_thread(task.save)
        return task
        


    def stop_process(self):
        if self.process:
            self.process.send_signal(signal.SIGTERM)


