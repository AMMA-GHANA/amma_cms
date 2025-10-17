from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Service, ServiceContentBlock


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


def service_detail(request, slug):
    """Display detailed service page with content blocks."""
    service = get_object_or_404(Service, slug=slug, is_active=True)

    # Get all active content blocks for this service
    content_blocks = service.content_blocks.filter(is_active=True).order_by('order')

    context = {
        'service': service,
        'content_blocks': content_blocks,
    }
    return render(request, 'services/detail.html', context)
