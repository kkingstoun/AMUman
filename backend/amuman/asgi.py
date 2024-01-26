"""
ASGI config for amuman project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amuman.settings")
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from manager.consumers import MasterConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Obsługa HTTP
    "websocket": URLRouter([
        path("ws/node/", MasterConsumer.as_asgi()),
    ]),
})
