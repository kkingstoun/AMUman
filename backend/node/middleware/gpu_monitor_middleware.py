from ..functions.gpu_monitor import GPUMonitor
import os
class GPUMonitorMiddleware:
    def __init__(self, get_response):
        pass
        # self.get_response = get_response
        # self.gpu_monitor = GPUMonitor()
        # self.gpu_monitor.submit_update_gpu_status(os.environ.get("NODE_ID"))

    def __call__(self, request):
        pass
        # Przypisz gpu_monitor do request, aby był dostępny w widokach
        # request.gpu_monitor = self.gpu_monitor
        # response = self.get_response(request)
        # return response