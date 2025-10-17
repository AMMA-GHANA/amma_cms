"""Decorators for staff portal access control"""

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from functools import wraps


def staff_required(view_func):
    """
    Decorator that requires user to be authenticated and staff member.
    Redirects to login if not authenticated, or 403 if not staff.
    """
    @wraps(view_func)
    @login_required(login_url='/admin/login/')
    @user_passes_test(lambda u: u.is_staff, login_url='/admin/login/')
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return wrapper
