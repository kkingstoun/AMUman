from celery import shared_task
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
@shared_task
def assign_tasks_to_gpus():
    # URL of the endpoint
    url = "http://localhost:8000/manager/send_command/"

    # Data to be sent (if needed)
    data = {
        'param1': 'value1',
        'param2': 'value2',
        # Add other parameters as required
    }

    # Make the POST request
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            # Handle success
            print("Command sent successfully:", response.json())
        else:
            # Handle failure
            print("Failed to send command:", response.text)
    except requests.exceptions.RequestException as e:
        # Handle request exceptions
        print("Error sending command:", e)

    
    # for gpu in free_gpus:
    #     for task in waiting_tasks:
    #         task.assigned_gpu_id = gpu.id
    #         task.status = "running"
    #         task.assigned_node_id = gpu.node_id
    #         task.save()

    #         gpu.task_id = task.id
    #         gpu.status = "busy"
    #         gpu.save()

    #         waiting_tasks = waiting_tasks.exclude(id=task.id)
    #         break
