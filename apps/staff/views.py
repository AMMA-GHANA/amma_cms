from django.shortcuts import render
from .models import StaffMember, Department


def staff_list(request):
    """Display list of all active staff members."""
    staff = StaffMember.objects.filter(
        is_active=True
    ).select_related('department').order_by('position_type', 'display_order', 'full_name')

    context = {
        'staff_members': staff,
        'departments': Department.objects.all(),
    }
    return render(request, 'staff/list.html', context)


def leadership_page(request):
    """Display leadership team page."""
    leadership = StaffMember.objects.filter(
        position_type='leadership',
        is_active=True
    ).select_related('department').order_by('display_order')

    management = StaffMember.objects.filter(
        position_type='management',
        is_active=True
    ).select_related('department').order_by('display_order')

    context = {
        'leadership': leadership,
        'management': management,
    }
    return render(request, 'staff/leadership.html', context)
