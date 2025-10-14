from django.shortcuts import render
from .models import Service


def service_list(request):
    """Display list of all active services."""
    services = Service.objects.filter(is_active=True).order_by('order', 'name')

    context = {
        'services': services,
    }
    return render(request, 'services/list.html', context)
