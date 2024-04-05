"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import mysite.routing

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Sostituisci "mysite" con il nome del tuo progetto Django

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # Django's ASGI application per gestire le richieste HTTP tradizionali
#     "websocket": AuthMiddlewareStack(  # AuthMiddlewareStack aggiunge il supporto per l'autenticazione utente
#         URLRouter(
#             mysite.routing.websocket_urlpatterns  # Il tuo routing WebSocket definito in myapp/routing.py
#         )
#     ),
# })

# mysite/asgi.py
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

import mysite.routing

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(mysite.routing.websocket_urlpatterns))
        ),
    }
)