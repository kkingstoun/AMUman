from channels.routing import ProtocolTypeRouter, URLRouter
from channels.middleware import ProtocolTypeRouter, MiddlewareStack
from myapp.middleware import WebSocketMiddleware
from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/node/', consumers.NodeConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        WebSocketMiddleware,
        path("ws/channel/", consumers.WebChannel.as_asgi()),  # Dodaj własne ścieżki WebSocket
    ]),
})
