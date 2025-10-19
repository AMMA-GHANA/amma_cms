"""Middleware for AMMA CMS Portal"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class RestrictAdminMiddleware:
    """
    Middleware to restrict Django admin access to superusers only.

    Portal users (is_staff=True but is_superuser=False) will be redirected
    to the AMMA CMS Portal instead of the Django admin panel.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is trying to access admin
        if request.path.startswith('/admin/'):
            # Allow if user is not authenticated (will be redirected to login)
            if not request.user.is_authenticated:
                return self.get_response(request)

            # Allow login page for all staff users
            if request.path.startswith('/admin/login/'):
                return self.get_response(request)

            # Allow logout page
            if request.path.startswith('/admin/logout/'):
                return self.get_response(request)

            # Block non-superusers from admin panel
            if not request.user.is_superuser:
                messages.warning(
                    request,
                    'You do not have permission to access the Django admin panel. '
                    'You have been redirected to the AMMA CMS Portal.'
                )
                return redirect('staff_portal:dashboard')

        response = self.get_response(request)
        return response
