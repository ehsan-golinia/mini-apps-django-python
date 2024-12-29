from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_dice, name='select_dice'),
    path('play/', views.dice_rolling_game, name='roll_dice'),
]
