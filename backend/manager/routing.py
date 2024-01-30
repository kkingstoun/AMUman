from django.urls import path
from .consumers import MasterConsumer

websocket_urlpatterns = [
    path('ws/node', MasterConsumer.as_asgi()),
]
