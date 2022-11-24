from django.urls import path
from . import views

urlpatterns = [
    path("suggest_activity", views.suggest_activity, name = "suggest-activity")
]
