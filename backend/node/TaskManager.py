import httpx
from asgiref.sync import sync_to_async
from django.conf import settings
import asyncio
from common_models.models import Task
import signal
import requests
import httpx
from datetime import datetime
from node.JobProcesss import JobProcess
import json
from subprocess import PIPE

class TaskManager:
    def __init__(self,node_id,*args, **kwargs):
        self.node_id=node_id
        self.url = f"http://localhost:8000/manager/task/"
        self.api_base_url = f"{settings.MANAGER_PORT}:{settings.MANAGER_PORT}"
        self.tasks={}

    async def execute_command(self, command, task_id):
        methods = {
            "run_task": self.run_task,
            # "cancel_task": self.cancel_task,
            # "redo_task": self.redo_task,
        }

        if command in methods:
            return await methods[command](task_id)
        else:
            return False
        
    async def run_task(self, task_id):
        task = await self.get_task(task_id)
        print(task)
        edit = await self.update_task_data()
        self.task = await self.run_simulation(task)
        edit = await self.update_task_data()
        # await self.start_simulation(task, gpu)

        # # Wyślij aktualizację do głównego hosta
        # await self.update_main_host(task)

        # return True
    async def run_simulation(self,task):
        
        job_process = JobProcess(task)
        await job_process.run_subprocess()

    async def get_task(self, task_id):
        url = f"{self.url}get_task/{task_id}/"
        self.task_id=task_id
        response = requests.get(url)
        try:
            if response.status_code == 200:
                task_data = response.json()
                self.task = Task(
                    id=task_data['id'],
                    user=task_data['user'],
                    path=task_data['path'],
                    node_name=task_data['node_name'],
                    port=task_data['port'],
                    submit_time=task_data['submit_time'],
                    start_time=task_data['start_time'],
                    end_time=task_data['end_time'],
                    error_time=task_data['error_time'],
                    priority=task_data['priority'],
                    gpu_partition=task_data['gpu_partition'],
                    est=task_data['est'],
                    status=task_data['status'],
                    assigned_node_id=task_data['assigned_node_id'],
                    assigned_gpu_id=task_data['assigned_gpu_id'],
                )
                await sync_to_async(self.task.save)()
                print("Successfully fetched task")
                return self.task
            else:
                print(f"Error fetching task: Status code {response.status_code}")
                self.task = None
        except Exception as e:
            print(e)
            self.task = None
    async def update_task_data(self,task=None):
        if task!= None:
            self.task=task
            status="Finished"
            output=task.output
        else:
            status="Running"
            output=None
            
        url = f"{self.url}edit_task/{self.task_id}/"
        data = {
            "status": status,
            "start_time": datetime.now().isoformat(),
            "port": "35367",
            "output": output,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data)
            print("Response Status Code:", response.status_code)
            try:
                print("Response JSON:", response.json())
                return response.json()
            except json.JSONDecodeError:
                print("Invalid JSON response")
                return None
            

    async def assign_gpu_to_task(self, task, gpu):
        task.assigned_gpu = gpu
        task.status = "Running"
        await sync_to_async(task.save)()

        gpu.status = "Busy"
        await sync_to_async(gpu.save)()

    async def start_simulation(self, task, gpu):
        # Logika rozpoczynania symulacji
        pass

    async def update_main_host(self, task):
        async with httpx.AsyncClient() as client:
            payload = {"task_id": task.id, "status": task.status}
            await client.post(f"{self.api_base_url}/update_task_status", json=payload)

