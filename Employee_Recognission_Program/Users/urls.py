from django.urls import path
from . import views

urlpatterns = [
    path("sign_up",views.register, name="register"),
    path("",views.login_view,name = "login"),
    path("logout",views.logout_view, name = "logout"),
    path("mass_upload_users",views.simple_upload , name = "mass_upload_users")
]
