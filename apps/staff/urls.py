"""URL configuration for staff app."""

from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.staff_list, name='list'),
    path('leadership/', views.leadership_page, name='leadership'),
]
