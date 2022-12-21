from django.urls import re_path

from .consumers import GameConsumer, GamePoolConsumer

websocket_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>\w+)/", GameConsumer.as_asgi()),
    re_path(r"ws/game_pool/", GamePoolConsumer.as_asgi()),
]
