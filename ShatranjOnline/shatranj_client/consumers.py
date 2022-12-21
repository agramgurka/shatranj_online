from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import logout

from .services.users import get_opponent, get_active_player, is_player
from .services.game_pool import set_winner, get_winner, get_moves_history, write_game, read_game, get_active_games, \
    is_opponent_connected, create_game, join_game, delete_game, active_game


class GameConsumer(AsyncJsonWebsocketConsumer):
    """ game consumer """

    async def connect(self) -> None:
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f'{self.game_id}'
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        await self.accept()

    async def receive_json(self, content, **kwargs) -> None:
        sender = self.scope['user']
        if await database_sync_to_async(is_player)(self.game_id, sender):
            game = await database_sync_to_async(read_game)(self.game_id)
            if not game.has_finished:
                active_player = await database_sync_to_async(get_active_player)(self.game_id)
                command = content['command']
                if command == 'init':
                    await self.send_json(
                        {
                            "command": "init",
                            "moves": await database_sync_to_async(get_moves_history)(self.game_id)
                        }
                    )
                if command == 'make_move':
                    move = content['move']
                    try:
                        if sender == active_player:
                            game.process_move(move)
                            if not game.has_started:
                                game.has_started = True
                            await database_sync_to_async(write_game)(self.game_id, game)
                            await self.channel_layer.group_send(
                                self.game_group_name,
                                {
                                    "type": "game.position",
                                    "position": game.render_position(),
                                    "move": game.last_move
                                }
                            )
                            if game.is_win():
                                await database_sync_to_async(set_winner)(self.game_id, sender)
                                await self.channel_layer.group_send(
                                    self.game_group_name,
                                    {
                                        "type": "game.over",
                                        "winner": await database_sync_to_async(get_winner)(self.game_id)
                                    }
                                )
                            if game.is_draw():
                                await self.channel_layer.group_send(
                                    self.game_group_name,
                                    {
                                        "type": "game.over",
                                        "winner": None
                                    }
                                )
                        else:
                            await self.send_json({"command": "error", "text": "not your turn"})
                    except ValueError:
                        await self.send_json({"command": "error", "text": "move is impossible"})

                if command == 'resign':
                    opponent = await database_sync_to_async(get_opponent)(self.game_id, sender)
                    game.has_finished = True
                    await database_sync_to_async(set_winner)(self.game_id, opponent)
                    await database_sync_to_async(write_game)(self.game_id, game)
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            "type": "game.over",
                            "winner": opponent.username
                        }
                    )
                if command == 'suggest_draw':
                    opponent = await database_sync_to_async(get_opponent)(self.game_id, sender)
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            "type": "suggest.draw",
                            "to": opponent.username
                        }
                    )
                if command == 'accept_draw':
                    game.has_finished = True
                    await database_sync_to_async(write_game)(self.game_id, game)
                    await self.channel_layer.group_send(
                        self.game_group_name,
                        {
                            "type": "game.over",
                            "winner": None
                        }
                    )
            else:
                await self.send_json(
                    {
                        "command": "over",
                        "winner": await database_sync_to_async(get_winner)(self.game_id)
                    }
                )

        else:
            await self.send_json({"command": "error", "text": "not a player"})

    async def game_position(self, event) -> None:
        """ sends game position """

        await self.send_json(
            {
                "command": "position",
                "position": event['position'],
                "move": event['move']
            }
        )

    async def game_over(self, event) -> None:
        """ sends message that game is over """

        await self.send_json(
            {
                "command": "over",
                "winner": event['winner']
            }
        )

    async def suggest_draw(self, event) -> None:
        """ send draw suggestion"""

        await self.send_json(
            {
                "command": "suggest_draw",
                "to": event['to']
            }
        )


class GamePoolConsumer(AsyncJsonWebsocketConsumer):
    """ active games consumer """

    async def receive_json(self, content, **kwargs) -> None:
        if self.scope['user'].is_authenticated:
            player_active_game = await database_sync_to_async(active_game)(self.scope['user'])
            if player_active_game:
                game_url = 'game/' + str(player_active_game)
                await self.send_json(
                    {
                        'command': 'start_game',
                        'game': game_url
                    }
                )
        command = content.get('command')
        if command == 'get_games':
            await self.send_json(
                    {
                        'command': 'active_games_update',
                        'active_games': await database_sync_to_async(get_active_games)(self.scope['user'])
                    }
                )
        if command == 'create':
            if self.scope['user'].is_authenticated:
                settings = content.get('settings', {})
                game_id = await database_sync_to_async(create_game)(self.scope['user'], settings)
                await self.send_json(
                    {
                        'command': 'game_created',
                        'game_id': game_id
                    }
                )
            else:
                await self.send_json(
                    {
                        'command': 'not_authorized',
                    }
                )
        if command == 'check_opponent':
            game_id = content['game_id']
            opponent_connected = await database_sync_to_async(is_opponent_connected)(game_id)
            if opponent_connected:
                game_url = 'game/' + str(game_id)
                await self.send_json(
                    {
                        'command': 'start_game',
                        'game': game_url
                    }
                )
        if command == 'cancel_created_game':
            game_id = content['game_id']
            await database_sync_to_async(delete_game)(game_id)
            await self.send_json(
                {
                    'command': 'game_cancelled',
                }
            )
        if command == 'join':
            if self.scope['user'].is_authenticated:
                game_id = content['game_id']
                if await database_sync_to_async(join_game)(game_id, self.scope['user']):
                    game_url = 'game/' + game_id
                    await self.send_json(
                        {
                            'command': 'start_game',
                            'game': game_url
                        }
                    )
            else:
                await self.send_json(
                    {
                        'command': 'not_authorized',
                    }
                )
        if command == 'log_out':
            await logout(self.scope)
