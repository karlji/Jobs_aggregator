from django.urls import path
from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("view", views.index, name="index"),
]
