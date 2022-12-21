""" database functions to work with game objects """
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db.models import Value, F, Q
from django.db.models.functions import Concat

from ..models import OnlineGameTable
from .engine import OnlineGame, PositionNotation, Color


def get_active_games(user: AbstractUser) -> Optional[list[dict]]:
    """ returns active games """

    if user.is_authenticated:
        games = OnlineGameTable.objects.filter(
            Q(has_started=False) &
            (
                    Q(white=None) |
                    Q(black=None)
            ) &
            ~Q(white=user) &
            ~Q(black=user)

        ).order_by('-created')
    else:
        games = OnlineGameTable.objects.filter(
            Q(has_started=False) &
            (
                    Q(white=None) |
                    Q(black=None)
            )
        ).order_by('-created')
    rendered_games = []
    for game in games:
        white = black = None
        if game.white:
            white = game.white.username
        if game.black:
            black = game.black.username
        rendered_games.append(
            {
                "id": game.id,
                "white": white,
                "black": black,
            }
        )
    return rendered_games


def is_opponent_connected(game_id: int) -> bool:
    """ check if opponent connected to a game """

    game = OnlineGameTable.objects.get(id=game_id)
    if game.white and game.black:
        return True
    return False


def create_game(player: AbstractUser, settings: dict) -> int:
    """ creates game and returns its id"""

    if 'position' in settings:
        if not settings['position']:
            settings.pop('position')
    game = OnlineGame(settings)
    player_color = settings.get('player1_color', 'WHITE').upper()
    if player_color == 'WHITE':
        white = player
        black = None
    else:
        white = None
        black = player
    new_game = OnlineGameTable.objects.create(
        board_cols=game.board.cols_count,
        board_rows=game.board.rows_count,
        turn=game.turn.name,
        has_started=game.has_started,
        has_finished=game.has_finished,
        position=game.board.position_notation,
        white=white,
        black=black,
        initial_position=game.board.position_notation,
    )
    return new_game.id


def join_game(game_id: int, player: AbstractUser) -> bool:
    """ joins active game """

    game = OnlineGameTable.objects.get(id=game_id)
    if game.white and game.white != player:
        game.black = player
    elif game.black and game.black != player:
        game.white = player
    game.save()
    return game.white and game.black


def delete_game(game_id: int) -> None:
    """ deletes game """

    OnlineGameTable.objects.get(id=game_id).delete()


def active_game(user: AbstractUser) -> Optional[int]:
    """ returns user's active game id, if there is one """

    active_games = OnlineGameTable.objects.filter(
        Q(white=user) | Q(black=user),
        has_finished=False,
    ).exclude(white=None).exclude(black=None)

    if active_games:
        return active_games[0].id


def read_game(game_id: int) -> OnlineGame:
    """ read game state from database """

    game_record = OnlineGameTable.objects.get(id=game_id)
    game_settings = {
        'board': {
            'cols': game_record.board_cols,
            'rows': game_record.board_rows,
        },
        'turn': Color[game_record.turn],
        'has_started': game_record.has_started,
        'has_finished': game_record.has_finished,
        'position': PositionNotation.from_notation(game_record.position),
    }
    game = OnlineGame(game_settings)
    return game


def write_game(game_id: int, game: OnlineGame) -> None:
    """ write game state into the base """

    OnlineGameTable.objects.filter(id=game_id).update(
        turn=game.turn.name,
        has_started=game.has_started,
        has_finished=game.has_finished,
        position=game.board.position_notation,
    )
    if game.last_move:
        OnlineGameTable.objects.filter(id=game_id).update(
            moves=Concat(F('moves'), Value('|'), Value(game.last_move))
        )


def get_player_color(game_id: int, user: AbstractUser) -> str:
    """ returns player's piece color """

    game = OnlineGameTable.objects.get(id=game_id)
    player_color = Color.WHITE.name
    if user == game.black:
        player_color = Color.BLACK.name
    return player_color


def set_winner(game_id: int, winner: AbstractUser) -> None:
    """ sets game winner """

    OnlineGameTable.objects.filter(id=game_id).update(winner=winner)


def get_winner(game_id: int) -> str:
    """ returns game winner's name """

    game = OnlineGameTable.objects.get(id=game_id)
    return game.winner.username


def get_moves_history(game_id: int) -> str:
    """ returns moves' history """

    game = OnlineGameTable.objects.get(id=game_id)
    return game.moves
