from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from auth_network.models import User


@database_sync_to_async
def get_user(user_id):
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None

@database_sync_to_async
def get_user_id(session):
    return session.get('user_id')


class CustomUserMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Misol uchun query string: ws://.../ws/chat/1/?user_id=5
        query = scope["query_string"].decode()

        user_id = await get_user_id(scope['session'])

        if user_id:
            scope["user"] = await get_user(user_id)
        else:
            scope["user"] = None

        return await super().__call__(scope, receive, send)