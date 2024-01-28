# import os
# from django.core.exceptions import MiddlewareNotUsed

# class WebSocketMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         if not (os.environ.get('RUN_MAIN') or 'runserver' in os.environ.get('DJANGO_SETTINGS_MODULE', '')):
#             raise MiddlewareNotUsed()
        
#         self.run_node_startup()
        
#     def __call__(self, request):
#         response = self.get_response(request)
#         if "websocket" in request.META.get('UPGRADE', '').lower():
#             print("WebSocket connection attempt.")
#         return response 
    
#     def run_node_startup(self):
#         # Tutaj umieść logikę zgłoszenia do managera
#         pass