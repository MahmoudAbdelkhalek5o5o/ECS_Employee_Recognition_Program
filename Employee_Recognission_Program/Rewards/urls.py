from django.urls import path
from . import views

urlpatterns = [
        path("view_vendors", views.view_vendors, name = "view-vendors"),
        path("view_rewards/<int:vendor_id>", views.view_rewards, name = "view_rewards"),
        path("suggest_vendor", views.suggest_vendor, name = "suggest-vendor"),

]
