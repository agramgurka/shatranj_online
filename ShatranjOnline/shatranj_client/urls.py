from django.urls import path
from .views import Game, Register, ActiveGamePool, Auth

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('auth/', Auth.as_view(), name='auth'),
    path('game/<int:pk>', Game.as_view(), name='game'),
    path('', ActiveGamePool.as_view(), name='active_games'),
]
