"""
ASGI config for manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from manager.consumers import ManagerConsumer
from manager.middleware.JWTAuthMiddleware import JwtAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amuman.settings")

application = ProtocolTypeRouter({
            "http": get_asgi_application(),
            "websocket": JwtAuthMiddleware(
                URLRouter([
                      path("ws/node/", ManagerConsumer.as_asgi()),
                ])
            ),
    }
)
