from django.shortcuts import render
from django.db.models import Q
from .models import Service


def service_list(request):
    """Display list of all active services with search functionality."""
    services = Service.objects.filter(is_active=True)

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Order results
    services = services.order_by('order', 'name')

    context = {
        'services': services,
        'search_query': search_query,
        'total_count': services.count(),
    }
    return render(request, 'services/list.html', context)
