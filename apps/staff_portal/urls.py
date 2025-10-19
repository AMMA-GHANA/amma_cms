"""URL configuration for staff portal"""

from django.urls import path
from . import views

app_name = 'staff_portal'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Authentication
    path('logout/', views.portal_logout, name='logout'),

    # Services Management
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    # API endpoints for live preview and AJAX operations
    path('api/services/preview/', views.service_preview_api, name='service_preview_api'),
    path('api/services/<int:pk>/blocks/reorder/', views.service_blocks_reorder_api, name='service_blocks_reorder_api'),
    path('api/templates/<str:template_key>/', views.get_template_api, name='get_template_api'),

    # News Management
    path('news/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:pk>/delete/', views.news_delete, name='news_delete'),

    # News API endpoints
    path('api/news/categories/create/', views.news_category_create_api, name='news_category_create_api'),

    # Projects Management
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Projects API endpoints
    path('api/projects/categories/create/', views.project_category_create_api, name='project_category_create_api'),
]
