from django.urls import path

from .consumers import ManagerConsumer

websocket_urlpatterns = [
    path("ws/node", ManagerConsumer.as_asgi()),
]
