"""Views for staff portal"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
import json

from apps.services.models import Service, ServiceContentBlock
from .decorators import staff_required
from .block_templates import get_all_templates, get_template


@staff_required
def dashboard(request):
    """Staff portal dashboard"""
    services_count = Service.objects.count()
    active_services_count = Service.objects.filter(is_active=True).count()

    context = {
        'services_count': services_count,
        'active_services_count': active_services_count,
    }
    return render(request, 'staff_portal/dashboard.html', context)


@staff_required
def service_list(request):
    """List all services for management"""
    services = Service.objects.all().order_by('order', 'name')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        services = services.filter(name__icontains=search_query)

    context = {
        'services': services,
        'search_query': search_query,
    }
    return render(request, 'staff_portal/services/list.html', context)


@staff_required
@require_http_methods(["GET", "POST"])
def service_create(request):
    """Create a new service"""
    if request.method == 'POST':
        return _save_service(request, None)

    # GET request - show form
    templates = get_all_templates()

    context = {
        'service': None,
        'content_blocks': [],
        'templates': templates,
        'is_create': True,
    }
    return render(request, 'staff_portal/services/edit.html', context)


@staff_required
@require_http_methods(["GET", "POST"])
def service_edit(request, pk):
    """Edit an existing service"""
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        return _save_service(request, service)

    # GET request - show form
    content_blocks = service.content_blocks.all().order_by('order')
    templates = get_all_templates()

    context = {
        'service': service,
        'content_blocks': content_blocks,
        'templates': templates,
        'is_create': False,
    }
    return render(request, 'staff_portal/services/edit.html', context)


def _save_service(request, service):
    """Helper function to save service and content blocks"""
    try:
        with transaction.atomic():
            # Get form data
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            icon = request.POST.get('icon', 'file-text')
            link_url = request.POST.get('link_url', '').strip()
            link_text = request.POST.get('link_text', 'Learn More')
            has_detail_page = request.POST.get('has_detail_page') == 'on'
            is_active = request.POST.get('is_active') == 'on'
            order = int(request.POST.get('order', 0))

            # Validate required fields
            if not name or not description:
                messages.error(request, 'Name and description are required.')
                return redirect(request.path)

            # Create or update service
            if service is None:
                service = Service()

            service.name = name
            service.description = description
            service.icon = icon
            service.link_url = link_url
            service.link_text = link_text
            service.has_detail_page = has_detail_page
            service.is_active = is_active
            service.order = order
            service.save()

            # Process content blocks
            blocks_data = request.POST.get('blocks_json', '[]')
            blocks = json.loads(blocks_data)

            # Delete existing blocks and create new ones
            service.content_blocks.all().delete()

            for block_data in blocks:
                ServiceContentBlock.objects.create(
                    service=service,
                    block_type=block_data.get('block_type', 'text'),
                    title=block_data.get('title', ''),
                    content=block_data.get('content', ''),
                    data=block_data.get('data', {}),
                    order=block_data.get('order', 0),
                    is_active=block_data.get('is_active', True)
                )

            messages.success(request, f'Service "{service.name}" saved successfully.')
            return redirect('staff_portal:service_list')

    except Exception as e:
        messages.error(request, f'Error saving service: {str(e)}')
        return redirect(request.path)


@staff_required
@require_POST
def service_delete(request, pk):
    """Delete a service"""
    service = get_object_or_404(Service, pk=pk)
    service_name = service.name
    service.delete()
    messages.success(request, f'Service "{service_name}" deleted successfully.')
    return redirect('staff_portal:service_list')


@staff_required
@require_POST
def service_preview_api(request):
    """API endpoint for live preview"""
    try:
        # Get service data from POST
        service_data = json.loads(request.POST.get('service_data', '{}'))
        blocks_data = json.loads(request.POST.get('blocks_data', '[]'))

        # Create temporary service object (not saved to DB)
        temp_service = Service(
            name=service_data.get('name', 'Service Name'),
            description=service_data.get('description', 'Service description'),
            icon=service_data.get('icon', 'file-text')
        )

        # Create temporary block objects
        temp_blocks = []
        for block_data in blocks_data:
            temp_blocks.append(ServiceContentBlock(
                block_type=block_data.get('block_type', 'text'),
                title=block_data.get('title', ''),
                content=block_data.get('content', ''),
                data=block_data.get('data', {}),
                order=block_data.get('order', 0)
            ))

        # Render preview HTML
        html = render_to_string('staff_portal/services/preview_content.html', {
            'service': temp_service,
            'content_blocks': temp_blocks
        })

        return JsonResponse({'success': True, 'html': html})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_required
@require_POST
def service_blocks_reorder_api(request, pk):
    """API endpoint for reordering blocks"""
    try:
        service = get_object_or_404(Service, pk=pk)
        block_orders = json.loads(request.POST.get('block_orders', '[]'))

        # Update block orders
        for item in block_orders:
            block_id = item.get('id')
            order = item.get('order')
            ServiceContentBlock.objects.filter(id=block_id, service=service).update(order=order)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@staff_required
def get_template_api(request, template_key):
    """API endpoint to get template data by key"""
    template = get_template(template_key)
    if template:
        return JsonResponse({
            'success': True,
            'template': template
        })
    return JsonResponse({
        'success': False,
        'error': 'Template not found'
    }, status=404)
