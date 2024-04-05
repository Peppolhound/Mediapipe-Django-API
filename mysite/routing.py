from django.urls import re_path
from .consumers import VideoStreamConsumer

websocket_urlpatterns = [
    re_path('ws/video/', VideoStreamConsumer.as_asgi()),
]