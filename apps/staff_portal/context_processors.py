"""Context processors for AMMA CMS Portal"""

from .permissions import (
    user_can_manage_news,
    user_can_manage_services,
    user_can_manage_projects,
    user_can_manage_documents,
    user_can_manage_staff
)


def portal_permissions(request):
    """
    Add portal permissions to template context.
    Makes permission checks available in all templates.
    """
    if not request.user.is_authenticated:
        return {
            'can_manage_news': False,
            'can_manage_services': False,
            'can_manage_projects': False,
            'can_manage_documents': False,
            'can_manage_staff': False,
        }

    return {
        'can_manage_news': user_can_manage_news(request.user),
        'can_manage_services': user_can_manage_services(request.user),
        'can_manage_projects': user_can_manage_projects(request.user),
        'can_manage_documents': user_can_manage_documents(request.user),
        'can_manage_staff': user_can_manage_staff(request.user),
    }
