from django.urls import path
from public import views



urlpatterns = [
    path('index', views.index_view, name="index"),
    path('home', views.home_view, name="home"),
]