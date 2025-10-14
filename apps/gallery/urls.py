"""URL configuration for gallery app."""

from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.gallery_list, name='list'),
    path('album/<slug:slug>/', views.album_detail, name='album'),
]
