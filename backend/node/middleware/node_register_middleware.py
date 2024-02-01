# app_name/middleware.py
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
import requests
from django.core.management.base import BaseCommand
from requests import get
from node.functions.gpu_monitor import GPUMonitor
import json
from django.core.exceptions import MiddlewareNotUsed
import os
import uuid
from dotenv import load_dotenv, set_key, get_key, find_dotenv


class NodeStartupMiddleware:
    def __init__(self, get_response):
        
        self.dotenv_file = find_dotenv()
        load_dotenv(self.dotenv_file)
        
        self.manager_url = os.getenv("MANAGER_URL") if os.getenv("MANAGER_URL") not in [None, ""] else "localhost:8000"
        self.node_id = os.getenv("NODE_ID") if os.getenv("NODE_ID") not in [None, ""] else "0" 
        self.node_name = os.getenv("NODE_NAME") if os.getenv("NODE_NAME") not in [None, ""] else str(uuid.uuid1())    
        
       
        self.node_management_url = f"http://{self.manager_url}/manager/node-management/"

        self.get_response = get_response

        if not (os.environ.get('RUN_MAIN') or 'runserver' in os.environ.get('DJANGO_SETTINGS_MODULE', '')):
            raise MiddlewareNotUsed("NodeStartupMiddleware is only used once.")
        self.run_node_startup()
        
    def __call__(self, request):
        response = self.get_response(request)
        return response

    def run_node_startup(self):
        url = self.node_management_url  
        data = {
            'action': "assign_new_node",
            'node_name':self.node_name,
            'ip': self.get_own_ip(),
            'port': None,  
            'number_of_gpus': 0,  
        }

        try:
            response = requests.post(url, data=data)
            response_data = response.json()
            if response.status_code == 200:
                os.environ["NODE_ID"] = str(response_data.get('id'))
                self.node_id=response_data.get('id')
                print('Successfull node assign. Response: ' + str(response_data.get('id')))
            elif response.status_code == 201:
                os.environ["NODE_ID"] = str(response_data.get('id'))
                self.node_id=response_data.get('id')
                print('Successfull node update. Response: ' + str(response_data))
            self.node_id=response_data.get('id')
            os.environ["NODE_ID"]=str(self.node_id)
            print(f'\033[92mSuccessfull found node_id: {self.node_id}.\033[0m')

            if response.status_code == 200:
                gpm = GPUMonitor() 
                gpm.assign_gpus(self.node_id)  
            elif response.status_code == 201:
                gpm = GPUMonitor() 
                gpm.submit_update_gpu_status(self.node_id)
                
        except requests.exceptions.RequestException as e:
            print(f'\033[92mBłąd: {e}.\033[0m')

    def get_own_ip(self):
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            print(f'\033[92mIP: {ip}.\033[0m')
            return ip
        except Exception as e:
            print(f"Błąd podczas pobierania własnego adresu IP: {e}")
            return EOFError
