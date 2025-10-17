"""
Context processors for Core app
Makes site settings available in all templates
"""

from .models import SiteSettings


def site_settings(request):
    """Make site settings available in all templates"""
    try:
        settings = SiteSettings.load()
    except Exception:
        settings = None

    return {
        'site_settings': settings,
        'is_homepage': request.path == '/',
    }
