from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from . import consumers

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/channel/", consumers.WebChannel.as_asgi()),  # Dodaj własne ścieżki WebSocket
    ]),
})
