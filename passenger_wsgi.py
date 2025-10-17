"""
Passenger WSGI file for cPanel Python deployment.
This is the entry point for your Django application on cPanel.
"""

import sys
import os

# Add your project directory to the sys.path
INTERP = os.path.expanduser("~/virtualenv/amma_cms/3.11/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set up paths
cwd = os.getcwd()
sys.path.insert(0, cwd)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Import and run Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
