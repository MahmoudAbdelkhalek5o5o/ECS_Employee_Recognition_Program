from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "users-home"),
    path("leaderboard", views.Leaderboard, name = "leaderboard")
]
