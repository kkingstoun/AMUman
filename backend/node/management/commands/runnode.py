import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Uruchom node i zgłoś do master'

    def add_arguments(self, parser):
        parser.add_argument('--ip', type=str, help='Adres IP mastera')
        parser.add_argument('--port', type=str, help='Port mastera')

    def handle(self, *args, **options):
        ip = options['ip'] if options['ip'] else 'localhost'
        port = options['port'] if options['port'] else '8000'
        gpu_info = 'Informacje o GPU'  # Tutaj logika do uzyskania informacji o GPU

        url = f'http://{ip}:{port}/master/assign_new_node'
        data = {
            'ip': ip,
            'port': port,
            'gpu_info': gpu_info,
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                self.stdout.write(self.style.SUCCESS('Pomyślnie zgłoszono node do mastera.'))
            else:
                self.stdout.write(self.style.ERROR('Niepowodzenie: ' + response.text))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Błąd: {e}'))
