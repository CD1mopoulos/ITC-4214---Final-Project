from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_game_view, name='add_game'),  # URL for adding games
]