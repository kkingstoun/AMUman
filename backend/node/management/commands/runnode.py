import requests
from django.core.management.base import BaseCommand
from django.conf import settings
import socket
from requests import get
from django.db import models
from common_models.models import Nodes
from node.functions.gpu_monitor import GPUMonitor

class Command(BaseCommand):
    help = 'Uruchom node i zgłoś do master'
    # def add_arguments(self, parser):
    #     parser.add_argument('--ip', type=str, help='Adres IP mastera')
    #     parser.add_argument('--port', type=str, help='Port mastera')

    def handle(self, *args, **options):
        # ip = options['ip'] if options['ip'] else 'localhost'
        # port = options['port'] if options['port'] else '8000'
        # local_port = settings.PORT #NEED TO BE TESTED!!!!!!!
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
        print(gpm.gpus_status)
        print(type(gpm.gpus_status))
        print(Nodes.objects.get(pk=node_id))
        for gpu_key, gpu in gpm.gpus_status.items():
            data = {
                'action': "assign_gpu",
                'brand_name': gpu['name'],
                'gpu_speed': None,  # Tutaj należy przypisać odpowiednią wartość
                'gpu_util': gpu['gpu_util'],
                'status': gpu['status'],
                'nodeid': Nodes.objects.get(pk=node_id),
                'is_running_amumax': gpu['is_running_amumax'],
            }
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