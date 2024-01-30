import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import socket
from requests import get
from django.db import models
from common_models.models import Nodes
from node.functions.gpu_monitor import GPUMonitor
import json
from django.core.cache import cache
import dotenv
import os
class Command(BaseCommand):
    
    def handle(self, *args, **options):
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        url = os.environ["NODE_MANAGEMENT_URL"]
        data = {
            'action':"assign_new_node",
            'ip': self.get_own_ip(),
            'port': None,
        }
        print("DUPAAA")
        try:
            response = requests.post(url, data=data)
            response_data = response.json()
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('Successfull node assign. Response: ' + str(response_data)))
            else:
                self.stdout.write(self.style.SUCCESS('Successfull node update. Response: ' + str(response_data)))
            
            dotenv.set_key(dotenv_file, "key", os.environ["key"])
            
            gpm = GPUMonitor()
            self.stdout.write(self.style.SUCCESS(f'Successfull found node_id: {local_setting.node_id}'))

            if response.status_code == 201:
                
                response_data = response.json()
                node_id =  os.environ["NODE_ID"]
                gpm.update_gpu_status(node_id)       
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Błąd: {e}'))
            
       

    def get_own_ip(self):
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            # own_ip = socket.gethostbyname(socket.gethostname())
            return ip
        except Exception as e:
            print(f"Błąd podczas pobierania własnego adresu IP: {e}")
            return EOFError
