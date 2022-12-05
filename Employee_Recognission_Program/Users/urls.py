from django.urls import path
from . import views

urlpatterns = [
    path("sign_up",views.register, name="register"),
    path("",views.login_view,name = "login"),
    path("logout",views.logout_view, name = "logout"),
    path("edit_pofile" , views.userEdit , name = "user_edit"),
    path("homescreen/change_password", views.change_password, name='change_password'),
    path('My_Points' , views.points_about_expire , name = "about_to_expire"),

]
