from django.urls import path
from . import views

urlpatterns = [
    path('', views.guessing_range, name='guessing_range'),
    path('play/', views.guess_number, name='guess_number'),
]
