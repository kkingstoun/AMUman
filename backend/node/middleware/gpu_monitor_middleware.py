from ..functions.gpu_monitor import GPUMonitor

class GPUMonitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.gpu_monitor = GPUMonitor()

    def __call__(self, request):
        # Przypisz gpu_monitor do request, aby był dostępny w widokach
        request.gpu_monitor = self.gpu_monitor
        response = self.get_response(request)
        return response