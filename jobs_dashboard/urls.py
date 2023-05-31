from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home_view"),
    path("search", views.search, name="search"),
    path("view", views.index, name="index"),
]
