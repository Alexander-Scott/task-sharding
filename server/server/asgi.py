"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
import task_director.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(URLRouter(task_director.routing.websocket_urlpatterns)),
        "channel": ChannelNameRouter(task_director.routing.channel_name_patterns),
    }
)
