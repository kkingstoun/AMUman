from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import parse_qs

@database_sync_to_async
def get_user_from_token(token):
    auth = JWTAuthentication()
    try:
        # W SimpleJWT, validated_token jest instancją Token, a nie słownikiem
        validated_token = auth.get_validated_token(token)
        user = auth.get_user(validated_token)
        return user
    except Exception as e:
        print(f"Exception in get_user_from_token: {e}")
        return AnonymousUser()

class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Rozpakuj token z query string lub headers
        query_string = parse_qs(scope['query_string'].decode())
        headers = dict(scope['headers'])
        
        token_key = None
        if 'token' in query_string:
            token_key = query_string['token'][0]  # Pobierz pierwszy token z listy
        elif b'authorization' in headers:
            # Zakładamy, że nagłówek Authorization jest w formacie "Bearer token"
            token_key = headers[b'authorization'].decode().split('Bearer ')[1]

        if token_key:
            scope['user'] = await get_user_from_token(token_key)
        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)
