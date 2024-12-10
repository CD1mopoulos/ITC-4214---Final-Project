from django.urls import path
from . import views
from django.urls import re_path

urlpatterns = [
    path('games/', views.games_list, name='games'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('rate/<int:game_id>/', views.rate_game, name='rate_game'),
    re_path(r'^games/(?P<genre>.+)/$', views.games, name='games_by_genre'),
    path('delete/<int:game_id>/', views.delete_game, name='delete_game'),
]
