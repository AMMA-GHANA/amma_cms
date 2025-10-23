"""Views for staff portal"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
import json

from apps.services.models import Service, ServiceContentBlock
from apps.news.models import NewsArticle, NewsCategory
from apps.projects.models import Project, ProjectCategory, ProjectImage
from apps.documents.models import Document, DocumentCategory
from apps.staff.models import StaffMember
from .decorators import (
    staff_required,
    portal_user_required,
    news_permission_required,
    services_permission_required,
    projects_permission_required,
    documents_permission_required
)
from .permissions import (
    user_can_manage_news,
    user_can_manage_services,
    user_can_manage_projects,
    user_can_manage_documents
)
from .block_templates import get_all_templates, get_template
from .forms import NewsArticleForm, ProjectForm, ProjectImageFormSet, DocumentForm


@portal_user_required
def dashboard(request):
    """AMMA CMS Portal dashboard"""
    # Check user permissions
    can_manage_news = user_can_manage_news(request.user)
    can_manage_services = user_can_manage_services(request.user)
    can_manage_projects = user_can_manage_projects(request.user)
    can_manage_documents = user_can_manage_documents(request.user)

    # Get statistics based on permissions
    services_count = Service.objects.count() if can_manage_services else 0
    active_services_count = Service.objects.filter(is_active=True).count() if can_manage_services else 0

    # News statistics
    news_count = NewsArticle.objects.count() if can_manage_news else 0
    published_news_count = NewsArticle.objects.filter(status='published').count() if can_manage_news else 0
    draft_news_count = NewsArticle.objects.filter(status='draft').count() if can_manage_news else 0

    # Project statistics
    projects_count = Project.objects.count() if can_manage_projects else 0
    ongoing_projects_count = Project.objects.filter(status='ongoing').count() if can_manage_projects else 0
    completed_projects_count = Project.objects.filter(status='completed').count() if can_manage_projects else 0

    # Document statistics
    documents_count = Document.objects.count() if can_manage_documents else 0
    public_documents_count = Document.objects.filter(is_public=True).count() if can_manage_documents else 0
    featured_documents_count = Document.objects.filter(is_featured=True).count() if can_manage_documents else 0

    context = {
        'services_count': services_count,
        'active_services_count': active_services_count,
        'news_count': news_count,
        'published_news_count': published_news_count,
        'draft_news_count': draft_news_count,
        'projects_count': projects_count,
        'ongoing_projects_count': ongoing_projects_count,
        'completed_projects_count': completed_projects_count,
        'documents_count': documents_count,
        'public_documents_count': public_documents_count,
        'featured_documents_count': featured_documents_count,
        # Permissions for template
        'can_manage_news': can_manage_news,
        'can_manage_services': can_manage_services,
        'can_manage_projects': can_manage_projects,
        'can_manage_documents': can_manage_documents,
    }
    return render(request, 'staff_portal/dashboard.html', context)


@services_permission_required
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


@services_permission_required
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


@services_permission_required
@require_http_methods(["GET", "POST"])
def service_edit(request, pk):
    """Edit an existing service"""
    service = get_object_or_404(Service, pk=pk)

    if request.method == 'POST':
        return _save_service(request, service)

    # GET request - show form
    content_blocks = service.content_blocks.all().order_by('order')
    templates = get_all_templates()

    # Serialize blocks to JSON for JavaScript
    content_blocks_json = [{
        'block_type': block.block_type,
        'title': block.title,
        'content': block.content,
        'data': block.data,
        'order': block.order
    } for block in content_blocks]

    context = {
        'service': service,
        'content_blocks': content_blocks,
        'content_blocks_json': content_blocks_json,
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


@services_permission_required
@require_POST
def service_delete(request, pk):
    """Delete a service"""
    service = get_object_or_404(Service, pk=pk)
    service_name = service.name
    service.delete()
    messages.success(request, f'Service "{service_name}" deleted successfully.')
    return redirect('staff_portal:service_list')


@services_permission_required
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


@services_permission_required
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


@services_permission_required
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


# ============================================================================
# NEWS MANAGEMENT VIEWS
# ============================================================================

@news_permission_required
def news_list(request):
    """List all news articles for management"""
    articles = NewsArticle.objects.all().select_related('category', 'author')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        articles = articles.filter(title__icontains=search_query)

    # Filter by status
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        articles = articles.filter(status=status_filter)

    # Filter by category
    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        articles = articles.filter(category_id=category_filter)

    # Order by most recent
    articles = articles.order_by('-created_at')

    # Get all categories for filter dropdown
    categories = NewsCategory.objects.all().order_by('name')

    context = {
        'articles': articles,
        'categories': categories,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
    }
    return render(request, 'staff_portal/news/list.html', context)


@news_permission_required
@require_http_methods(["GET", "POST"])
def news_create(request):
    """Create a new news article"""
    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" created successfully.')
            return redirect('staff_portal:news_list')
    else:
        form = NewsArticleForm()

    context = {
        'form': form,
        'article': None,
        'is_create': True,
    }
    return render(request, 'staff_portal/news/edit.html', context)


@news_permission_required
@require_http_methods(["GET", "POST"])
def news_edit(request, pk):
    """Edit an existing news article"""
    article = get_object_or_404(NewsArticle, pk=pk)

    if request.method == 'POST':
        form = NewsArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Article "{article.title}" updated successfully.')
            return redirect('staff_portal:news_list')
    else:
        form = NewsArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
        'is_create': False,
    }
    return render(request, 'staff_portal/news/edit.html', context)


@news_permission_required
@require_POST
def news_delete(request, pk):
    """Delete a news article"""
    article = get_object_or_404(NewsArticle, pk=pk)
    article_title = article.title
    article.delete()
    messages.success(request, f'Article "{article_title}" deleted successfully.')
    return redirect('staff_portal:news_list')


@news_permission_required
@require_POST
def news_category_create_api(request):
    """API endpoint to create a new category"""
    try:
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        color = request.POST.get('color', '#d4af37').strip()

        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Category name is required'
            }, status=400)

        # Check if category already exists
        if NewsCategory.objects.filter(name=name).exists():
            return JsonResponse({
                'success': False,
                'error': 'A category with this name already exists'
            }, status=400)

        category = NewsCategory.objects.create(
            name=name,
            description=description,
            color=color
        )

        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# PROJECT MANAGEMENT VIEWS
# ============================================================================

@projects_permission_required
def project_list(request):
    """List all projects for management"""
    projects = Project.objects.all().select_related('category')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        projects = projects.filter(title__icontains=search_query)

    # Filter by status
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        projects = projects.filter(status=status_filter)

    # Filter by category
    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        projects = projects.filter(category_id=category_filter)

    # Order by featured, then order field
    projects = projects.order_by('-is_featured', 'order', '-start_date')

    # Get all categories for filter dropdown
    categories = ProjectCategory.objects.all().order_by('name')

    context = {
        'projects': projects,
        'categories': categories,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
    }
    return render(request, 'staff_portal/projects/list.html', context)


@projects_permission_required
@require_http_methods(["GET", "POST"])
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        formset = ProjectImageFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                project = form.save()
                formset.instance = project
                formset.save()

            messages.success(request, f'Project "{project.title}" created successfully.')
            return redirect('staff_portal:project_list')
    else:
        form = ProjectForm()
        formset = ProjectImageFormSet()

    context = {
        'form': form,
        'formset': formset,
        'project': None,
        'is_create': True,
    }
    return render(request, 'staff_portal/projects/edit.html', context)


@projects_permission_required
@require_http_methods(["GET", "POST"])
def project_edit(request, pk):
    """Edit an existing project"""
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=project)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                project = form.save()
                formset.save()

            messages.success(request, f'Project "{project.title}" updated successfully.')
            return redirect('staff_portal:project_list')
    else:
        form = ProjectForm(instance=project)
        formset = ProjectImageFormSet(instance=project)

    context = {
        'form': form,
        'formset': formset,
        'project': project,
        'is_create': False,
    }
    return render(request, 'staff_portal/projects/edit.html', context)


@projects_permission_required
@require_POST
def project_delete(request, pk):
    """Delete a project"""
    project = get_object_or_404(Project, pk=pk)
    project_title = project.title
    project.delete()
    messages.success(request, f'Project "{project_title}" deleted successfully.')
    return redirect('staff_portal:project_list')


@projects_permission_required
@require_POST
def project_category_create_api(request):
    """API endpoint to create a new project category"""
    try:
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', 'building').strip()
        color = request.POST.get('color', '#d4af37').strip()

        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Category name is required'
            }, status=400)

        # Check if category already exists
        if ProjectCategory.objects.filter(name=name).exists():
            return JsonResponse({
                'success': False,
                'error': 'A category with this name already exists'
            }, status=400)

        category = ProjectCategory.objects.create(
            name=name,
            description=description,
            icon=icon,
            color=color
        )

        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# DOCUMENT MANAGEMENT VIEWS
# ============================================================================

@documents_permission_required
def document_list(request):
    """List all documents for management"""
    documents = Document.objects.all().select_related('category')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        documents = documents.filter(title__icontains=search_query)

    # Filter by category
    category_filter = request.GET.get('category', '').strip()
    if category_filter:
        documents = documents.filter(category_id=category_filter)

    # Filter by year
    year_filter = request.GET.get('year', '').strip()
    if year_filter:
        documents = documents.filter(document_year=year_filter)

    # Filter by public status
    public_filter = request.GET.get('public', '').strip()
    if public_filter == 'public':
        documents = documents.filter(is_public=True)
    elif public_filter == 'private':
        documents = documents.filter(is_public=False)

    # Order by most recent
    documents = documents.order_by('-uploaded_date')

    # Get all categories for filter dropdown
    categories = DocumentCategory.objects.all().order_by('name')

    # Get available years for filter
    years = Document.objects.values_list('document_year', flat=True).distinct().order_by('-document_year')
    years = [year for year in years if year is not None]

    context = {
        'documents': documents,
        'categories': categories,
        'years': years,
        'search_query': search_query,
        'category_filter': category_filter,
        'year_filter': year_filter,
        'public_filter': public_filter,
    }
    return render(request, 'staff_portal/documents/list.html', context)


@documents_permission_required
@require_http_methods(["GET", "POST"])
def document_create(request):
    """Create a new document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.title}" created successfully.')
            return redirect('staff_portal:document_list')
    else:
        form = DocumentForm()

    context = {
        'form': form,
        'document': None,
        'is_create': True,
    }
    return render(request, 'staff_portal/documents/edit.html', context)


@documents_permission_required
@require_http_methods(["GET", "POST"])
def document_edit(request, pk):
    """Edit an existing document"""
    document = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            document = form.save()
            messages.success(request, f'Document "{document.title}" updated successfully.')
            return redirect('staff_portal:document_list')
    else:
        form = DocumentForm(instance=document)

    context = {
        'form': form,
        'document': document,
        'is_create': False,
    }
    return render(request, 'staff_portal/documents/edit.html', context)


@documents_permission_required
@require_POST
def document_delete(request, pk):
    """Delete a document"""
    document = get_object_or_404(Document, pk=pk)
    document_title = document.title
    document.delete()
    messages.success(request, f'Document "{document_title}" deleted successfully.')
    return redirect('staff_portal:document_list')


@documents_permission_required
@require_POST
def document_category_create_api(request):
    """API endpoint to create a new document category"""
    try:
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        icon = request.POST.get('icon', 'folder').strip()

        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Category name is required'
            }, status=400)

        # Check if category already exists
        if DocumentCategory.objects.filter(name=name).exists():
            return JsonResponse({
                'success': False,
                'error': 'A category with this name already exists'
            }, status=400)

        category = DocumentCategory.objects.create(
            name=name,
            description=description,
            icon=icon
        )

        return JsonResponse({
            'success': True,
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def portal_logout(request):
    """
    Logout view for AMMA CMS Portal users.
    Logs out the user and redirects to the login page with a success message.
    """
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('/admin/login/')
