import logging

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication

log = logging.getLogger("rich")


@database_sync_to_async
def get_user_from_token(token):
    try:
        auth = JWTAuthentication()
        validated_token = auth.get_validated_token(token)
        user = auth.get_user(validated_token)
        return user
    except Exception as e:
        log.debug(f"Exception in get_user_from_token: {e}")
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            token_key = (
                dict(scope["headers"])[b"authorization"].decode().split("Bearer ")[1]
            )
            log.debug("WEBSOCKET: Token found.")
            scope["user"] = await get_user_from_token(token_key)
            log.debug(f"WEBSOCKET: User: {scope['user']}")

        except Exception:
            log.debug("WEBSOCKET: Token not found.")
            scope["user"] = AnonymousUser()
            token_key = None

        return await super().__call__(scope, receive, send)
