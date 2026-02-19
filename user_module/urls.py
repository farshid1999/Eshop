from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelView.as_view(), name='user_page'),
    path('add-favorite', views.add_to_favorite, name='add_favorite'),
    path("get-cities/", views.get_cities, name="get_cities"),
]
