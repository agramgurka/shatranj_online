from django.db import models
from django.contrib.auth.models import User


class OnlineGameTable(models.Model):
    """ table represents shatranj online game """

    board_cols = models.IntegerField('cols')
    board_rows = models.IntegerField('rows')
    turn = models.CharField('turn', max_length=100)
    has_started = models.BooleanField('has started', default=False)
    has_finished = models.BooleanField('has finished', default=False)
    position = models.CharField('position', max_length=1000)
    white = models.ForeignKey(User, on_delete=models.CASCADE, related_name='white_games', null=True, default=None)
    black = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='black_games', null=True, default=None)
    initial_position = models.CharField('position', max_length=1000, default="")
    moves = models.CharField('moves', max_length=2000, default="")
    winner = models.ForeignKey(User, related_name='won_games', null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField('created', auto_now_add=True)
