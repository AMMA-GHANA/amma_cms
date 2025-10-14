"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize admin site
admin.site.site_header = "AMMA CMS Administration"
admin.site.site_title = "AMMA CMS Admin"
admin.site.index_title = "Welcome to AMMA Content Management System"

urlpatterns = [
    # Core pages (homepage, about)
    path('', include('apps.core.urls')),

    # App URLs
    path('news/', include('apps.news.urls')),
    path('projects/', include('apps.projects.urls')),
    path('staff/', include('apps.staff.urls')),
    path('services/', include('apps.services.urls')),
    path('documents/', include('apps.documents.urls')),
    path('gallery/', include('apps.gallery.urls')),
    path('contact/', include('apps.contact.urls')),

    # Admin and CKEditor
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]

# Development-only URLs
if settings.DEBUG:
    # Serve media and static files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Django Debug Toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
        ]
