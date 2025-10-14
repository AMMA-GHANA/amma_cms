"""
Development settings for AMMA CMS project.
"""

from .base import *

# Development-specific settings
DEBUG = True

# Additional apps for development
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

# Debug Toolbar Middleware
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Internal IPs for Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Development email backend (console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow all hosts in development
ALLOWED_HOSTS = ['*']
