import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import socket
from requests import get
from django.db import models
from common_models.models import Nodes
from node.functions.gpu_monitor import GPUMonitor
import json

class Command(BaseCommand):
    
    def add_arguments(self, parser):
        parser.add_argument('--ip', type=str, help='Adres IP mastera')
        parser.add_argument('--port', type=str, help='Port mastera')

    def handle(self, *args, **options):
        ip = options.get('ip', 'localhost')  # Użyj 'localhost' jako wartości domyślnej, jeśli 'ip' nie istnieje
        port = options.get('port', '8000')  # Użyj '8000' jako wartości domyślnej, jeśli 'port' nie istnieje
        local_port = settings.PORT #NEED TO BE TESTED!!!!!!!
        url = f'http://localhost:8000/master/node-management/'
        data = {
            'action':"assign_new_node",
            'ip': self.get_own_ip(),
            'port': None,
            'number_of_gpus': 0,
        }
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                response_data = response.json()
                node_id = response_data.get('id')
                self.stdout.write(self.style.SUCCESS('Pomyślnie zgłoszono node do mastera. Response: ' + str(response_data)))
            else:
                self.stdout.write(self.style.ERROR('Niepowodzenie: ' + response.text))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Błąd: {e}'))
            
        gpm = GPUMonitor()
        for gpu_key, gpu in gpm.gpus_status.items():
            data = {
                'action': "assign_gpu",
                'brand_name': gpu['name'],
                'gpu_speed': None,  # Tutaj należy przypisać odpowiednią wartość
                'gpu_util': gpu['gpu_util'],
                'status': gpu['status'],
                'node_id': node_id,
                'is_running_amumax': gpu['is_running_amumax'],
                'gpu_id': gpu_key,
                'gpu_info':None,
            }
            # print(json.dumps(data) )
            try:
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    response_data = response.json()
                    self.stdout.write(self.style.SUCCESS('Successfull gpu assign. Response: ' + str(response_data)))
                else:
                    self.stdout.write(self.style.ERROR('Error: ' + response.text))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))

    def get_own_ip(self):
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            # own_ip = socket.gethostbyname(socket.gethostname())
            return ip
        except Exception as e:
            print(f"Błąd podczas pobierania własnego adresu IP: {e}")
            return EOFError