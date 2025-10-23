# Generated migration for adding documents management permission

from django.db import migrations


def create_documents_permission(apps, schema_editor):
    """Create custom permission for document management"""
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Get content type for Group model (we attach custom perms to it)
    content_type = ContentType.objects.get(
        app_label='auth',
        model='group'
    )

    # Create documents permission
    Permission.objects.get_or_create(
        codename='can_manage_documents',
        content_type=content_type,
        defaults={'name': 'Can manage documents'}
    )


def remove_documents_permission(apps, schema_editor):
    """Remove documents permission (for migration rollback)"""
    Permission = apps.get_model('auth', 'Permission')

    # Delete the permission
    Permission.objects.filter(
        codename='can_manage_documents'
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('staff_portal', '0001_add_portal_permissions'),
        ('auth', '__latest__'),
        ('contenttypes', '__latest__'),
    ]

    operations = [
        migrations.RunPython(create_documents_permission, remove_documents_permission),
    ]
