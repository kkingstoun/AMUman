# middleware.py
# import .node_register_middleware
class WebSocketMiddleware:
    def __init__(self, get_response):
        # node_register_middleware.register_middleware(self)
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if "websocket" in request.META.get('UPGRADE', '').lower():
            print("WebSocket connection attempt.")
        return response 