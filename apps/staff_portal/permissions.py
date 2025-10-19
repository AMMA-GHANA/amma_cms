"""Custom permissions for AMMA CMS Portal"""

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class PortalPermissions:
    """
    Custom permissions for portal users.
    These define what content portal users can manage.
    """

    # Permission codenames
    CAN_MANAGE_NEWS = 'can_manage_news'
    CAN_MANAGE_SERVICES = 'can_manage_services'
    CAN_MANAGE_PROJECTS = 'can_manage_projects'

    # Permission definitions
    PERMISSIONS = [
        (CAN_MANAGE_NEWS, 'Can manage news articles'),
        (CAN_MANAGE_SERVICES, 'Can manage services'),
        (CAN_MANAGE_PROJECTS, 'Can manage projects'),
    ]

    @classmethod
    def create_permissions(cls):
        """
        Create custom permissions in the database.
        This should be called in a data migration.
        """
        from django.contrib.auth.models import Group

        # Get or create a content type for our custom permissions
        # We'll attach them to the Group model since they're not model-specific
        content_type = ContentType.objects.get_for_model(Group)

        created_permissions = []
        for codename, name in cls.PERMISSIONS:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )
            created_permissions.append(permission)
            if created:
                print(f"Created permission: {name}")

        return created_permissions


def user_can_manage_news(user):
    """Check if user has permission to manage news"""
    return user.is_superuser or user.has_perm(f'auth.{PortalPermissions.CAN_MANAGE_NEWS}')


def user_can_manage_services(user):
    """Check if user has permission to manage services"""
    return user.is_superuser or user.has_perm(f'auth.{PortalPermissions.CAN_MANAGE_SERVICES}')


def user_can_manage_projects(user):
    """Check if user has permission to manage projects"""
    return user.is_superuser or user.has_perm(f'auth.{PortalPermissions.CAN_MANAGE_PROJECTS}')
