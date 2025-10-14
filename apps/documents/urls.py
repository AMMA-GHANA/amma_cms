"""URL configuration for documents app."""

from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.document_list, name='list'),
    path('download/<int:pk>/', views.document_download, name='download'),
]
