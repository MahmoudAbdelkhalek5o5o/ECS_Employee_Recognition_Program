from django.urls import path
from . import views

urlpatterns = [
    path('categories_view',views.categories_view,name = 'categories_view'),
    path('category_activities_view/<int:category_id>', views.category_activities_view, name='category_activities_view'),
    path('submit_activity_request/<int:activity_id>', views.submit_activity_request, name = "submit_activity_request"),
    path("suggest_activity", views.suggest_activity, name = "suggest-activity"),
    path("view_activity_requests", views.view_activity_requests, name = "view_activity_requests"),
    path("accept_activity_request/<int:request_id>", views.accept_activity_request, name = "accept_activity_request"),
    path("decline_activity_request/<int:request_id>", views.decline_activity_request, name = "decline_activity_request"),

]
