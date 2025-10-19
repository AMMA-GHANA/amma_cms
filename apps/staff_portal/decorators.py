"""Decorators for AMMA CMS Portal access control"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps

from .permissions import (
    user_can_manage_news,
    user_can_manage_services,
    user_can_manage_projects
)


def portal_user_required(view_func):
    """
    Decorator that requires user to be authenticated and a portal user.
    Portal users are staff members (is_staff=True) who can access the portal.
    Redirects to login if not authenticated.
    """
    @wraps(view_func)
    @login_required(login_url='/admin/login/')
    @user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper


# Keep staff_required as alias for backwards compatibility
staff_required = portal_user_required


def permission_required_for_portal(permission_check_func, error_message=None):
    """
    Decorator factory for permission-based access control.

    Args:
        permission_check_func: Function that takes a user and returns True/False
        error_message: Custom error message to display if permission denied
    """
    def decorator(view_func):
        @wraps(view_func)
        @portal_user_required
        def wrapper(request, *args, **kwargs):
            if not permission_check_func(request.user):
                if error_message:
                    messages.error(request, error_message)
                else:
                    messages.error(
                        request,
                        'You do not have permission to access this section.'
                    )
                return redirect('staff_portal:dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def news_permission_required(view_func):
    """Decorator that requires permission to manage news"""
    return permission_required_for_portal(
        user_can_manage_news,
        'You do not have permission to manage news articles.'
    )(view_func)


def services_permission_required(view_func):
    """Decorator that requires permission to manage services"""
    return permission_required_for_portal(
        user_can_manage_services,
        'You do not have permission to manage services.'
    )(view_func)


def projects_permission_required(view_func):
    """Decorator that requires permission to manage projects"""
    return permission_required_for_portal(
        user_can_manage_projects,
        'You do not have permission to manage projects.'
    )(view_func)
