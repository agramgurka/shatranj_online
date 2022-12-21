import json

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView
from django.contrib.auth import login, authenticate

from .models import OnlineGameTable
from .services.game_pool import read_game, get_player_color
from .services.users import create_user


class Auth(View):
    """ user's authentication view """

    def post(self, request):
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        return redirect('active_games')


class Register(View):
    """ user's registration view """

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user_login = request.POST['login']
        user_password = request.POST['password']
        try:
            create_user(login=user_login, password=user_password)
            return redirect('active_games')
        except ValueError:
            return render(request, 'register.html')


class ActiveGamePool(View):
    """ active games view """

    def get(self, request):
        return render(
            request, 'game_pool.html',
            {
                "username": request.user.username,
                "authorized": json.dumps(request.user.is_authenticated)
            }
        )


class Game(DetailView):
    """ game representation view """

    model = OnlineGameTable
    template_name = 'board.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        game_id = self.kwargs['pk']
        game = read_game(game_id)
        board = json.dumps(game.render_board())
        position = json.dumps(game.render_position())
        player_color = json.dumps(get_player_color(game_id, request.user))
        username = json.dumps(request.user.username)
        turn = json.dumps(game.turn.name)
        context = self.get_context_data(
            board=board,
            position=position,
            player_color=player_color,
            username=username,
            turn=turn
        )
        return self.render_to_response(context)
