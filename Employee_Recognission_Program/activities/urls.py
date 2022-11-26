from django.urls import path
from . import views

urlpatterns = [
    path('categories_view',views.categories_view,name = 'categories_view'),
    path('category_activities_view/<int:category_id>', views.category_activities_view, name='category_activities_view'),
    path('submit_activity_request/<int:activity_id>', views.submit_activity_request, name = "submit_activity_request"),
    path("suggest_activity", views.suggest_activity, name = "suggest-activity"),
]
