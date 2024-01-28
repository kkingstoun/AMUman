import threading
import time
import requests

def send_command_to_master():
    url = "http://localhost:8000/manager/send_command/"
    # Dodaj odpowiednie parametry zgodnie z potrzebami
    data = {"param1": "value1", "param2": "value2"}
    try:
        response = requests.post(url, data=data)
        print("Response from Master:", response.text)
    except requests.RequestException as e:
        print("Error sending command to master:", e)

class RepeatTimer(threading.Timer):
    def __init__(self, interval, function, *args, **kwargs):
        threading.Timer.__init__(self, interval, function, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                return
            self.function(*self.args, **self.kwargs)

def start_scheduler():
    timer = RepeatTimer(30, send_command_to_master)  # Uruchom co 30 sekund
    timer.start()
