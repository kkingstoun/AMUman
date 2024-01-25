# node/routing.py

from django.urls import path
from .consumers import NodeConsumer

websocket_urlpatterns = [
    path('ws/some-path/', NodeConsumer.as_asgi()),
]