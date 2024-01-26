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
from node.models import Local

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--ip', type=str, help='Adres IP managera')
        parser.add_argument('--port', type=str, help='Port managera')

    def handle(self, *args, **options):
        ip = options.get('ip', 'localhost')  # Użyj 'localhost' jako wartości domyślnej, jeśli 'ip' nie istnieje
        port = options.get('port', '8000')  # Użyj '8000' jako wartości domyślnej, jeśli 'port' nie istnieje
        local_port = settings.PORT #NEED TO BE TESTED!!!!!!!
        url = f'http://localhost:8000/manager/node-management/'
        gpm = GPUMonitor()
        data = {
            'action':"assign_new_node",
            'ip': self.get_own_ip(),
            'port': None,
            'number_of_gpus': gpm.number_of_gpus,
        }
        try:
            response = requests.post(url, data=data)
            response_data = response.json()
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('Successfull node assign. Response: ' + str(response_data)))
            else:
                self.stdout.write(self.style.SUCCESS('Successfull node update. Response: ' + str(response_data)))
            
            local_setting, created = Local.objects.get_or_create(id=1)
            local_setting.node_id = response_data.get('id')
            local_setting.url = url
            local_setting.save()
            
            self.stdout.write(self.style.SUCCESS(f'Successfull found node_id: {local_setting.node_id}'))

            if response.status_code == 201:
                
                response_data = response.json()
                node_id =  local_setting.node_id 
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