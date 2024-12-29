from django.urls import path
from . import views

urlpatterns = [
    path('', views.player_settings, name='player_settings'),
    path('play/', views.rock_paper_scissors, name='rock_paper_scissors'),
]
