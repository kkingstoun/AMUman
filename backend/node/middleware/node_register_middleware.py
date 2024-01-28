# app_name/middleware.py
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
import requests
from django.core.management.base import BaseCommand
from requests import get
from node.models import Local
from node.functions.gpu_monitor import GPUMonitor
import json
from django.core.exceptions import MiddlewareNotUsed

class NodeStartupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.run_node_startup()
        raise MiddlewareNotUsed("NodeStartupMiddleware is only used once.")

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def run_node_startup(self):
        ip = 'localhost'  # Zastąp localhost swoim adresem IP, jeśli jest inny
        port = '8000'  # Zastąp 8000 swoim portem, jeśli jest inny
        url = f'http://{ip}:{port}/manager/node-management/'    
        data = {
            'action': "assign_new_node",
            'ip': self.get_own_ip(),
            'port': None,  # Możesz zastąpić None właściwym portem, jeśli jest potrzebny
            'number_of_gpus': 0,  # Zaktualizuj tę wartość odpowiednio
        }

        try:
            response = requests.post(url, data=data)
            response_data = response.json()
            # if response.status_code == 200:
            #     print('Successfull node assign. Response: ' + str(response_data.id))
            # else:
            #     print('Successfull node update. Response: ' + str(response_data))
            
            local_setting, created = Local.objects.get_or_create(id=1)
            local_setting.node_id = response_data.get('id')
            local_setting.managerNmUrl = url
            local_setting.save()
            
            print(f'\033[92mSuccessfull found node_id: {local_setting.node_id}.\033[0m')

            if response.status_code == 201:
                node_id =  local_setting.node_id
                gpm = GPUMonitor() 
                gpm.assign_gpus(node_id)       
        except requests.exceptions.RequestException as e:
            print(f'\033[92mBłąd: {e}.\033[0m')

    def get_own_ip(self):
        try:
            ip = get('https://api.ipify.org').content.decode('utf8')
            return ip
        except Exception as e:
            print(f"Błąd podczas pobierania własnego adresu IP: {e}")
            return EOFError
