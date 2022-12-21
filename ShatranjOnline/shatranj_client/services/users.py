""" database functions to work with user objects """

from typing import Optional

from django.contrib.auth.models import User, AbstractUser

from ..models import OnlineGameTable


def create_user(login: str, password: str) -> Optional[User]:
    """ creates new user """

    if not User.objects.filter(username=login).exists():
        user = User.objects.create_user(username=login, password=password)
        return user
    raise ValueError('login is occupied')


def get_active_player(game_id: int) -> User:
    """ returns active player"""

    game = OnlineGameTable.objects.get(id=game_id)
    if game.turn == 'WHITE':
        return game.white
    return game.black


def get_opponent(game_id: int, player: AbstractUser) -> Optional[User]:
    """ returns player's opponent """

    game = OnlineGameTable.objects.get(id=game_id)
    if player == game.white:
        return game.black
    if player == game.black:
        return game.white


def is_player(game_id: int, user: AbstractUser) -> bool:
    """ check if user is player """

    game = OnlineGameTable.objects.get(id=game_id)
    return user in (game.white, game.black)
