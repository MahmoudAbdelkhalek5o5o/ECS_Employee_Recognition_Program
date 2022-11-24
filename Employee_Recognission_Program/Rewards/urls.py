from django.urls import path
from . import views

urlpatterns = [
        path("suggest_vendor", views.suggest_vendor, name = "suggest-vendor"),

]
