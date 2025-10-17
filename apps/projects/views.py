from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Project, ProjectCategory


def project_list(request):
    """Display list of projects with search, filtering, sorting, and pagination."""
    projects = Project.objects.select_related('category').prefetch_related('images').all()

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(detailed_description__icontains=search_query)
        )

    # Filter by category
    selected_category = None
    category_slug = request.GET.get('category')
    if category_slug:
        selected_category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=selected_category)

    # Filter by status
    selected_status = request.GET.get('status', '').strip()
    if selected_status and selected_status in ['planned', 'ongoing', 'completed', 'suspended']:
        projects = projects.filter(status=selected_status)

    # Sorting
    sort_by = request.GET.get('sort', '-is_featured')
    valid_sort_options = ['-is_featured', '-start_date', 'start_date', '-budget', 'budget', 'title', '-title']
    if sort_by in valid_sort_options:
        # Handle compound sorting for featured items
        if sort_by == '-is_featured':
            projects = projects.order_by('-is_featured', 'order', '-start_date')
        else:
            projects = projects.order_by(sort_by)
    else:
        projects = projects.order_by('-is_featured', 'order', '-start_date')

    # Get categories with project counts
    categories = ProjectCategory.objects.annotate(
        project_count=Count('projects')
    ).order_by('order', 'name')

    # Get status counts for filter display
    status_counts = {
        'all': Project.objects.count(),
        'planned': Project.objects.filter(status='planned').count(),
        'ongoing': Project.objects.filter(status='ongoing').count(),
        'completed': Project.objects.filter(status='completed').count(),
        'suspended': Project.objects.filter(status='suspended').count(),
    }

    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'selected_status': selected_status,
        'search_query': search_query,
        'sort_by': sort_by,
        'status_counts': status_counts,
        'total_count': paginator.count,
    }
    return render(request, 'projects/list.html', context)


def project_detail(request, slug):
    """Display single project detail."""
    project = get_object_or_404(
        Project.objects.select_related('category').prefetch_related('images'),
        slug=slug
    )

    # Related projects
    related = Project.objects.filter(
        category=project.category
    ).exclude(pk=project.pk).prefetch_related('images').order_by('-is_featured', 'order')[:3]

    context = {
        'project': project,
        'related_projects': related,
    }
    return render(request, 'projects/detail.html', context)


def project_by_category(request, slug):
    """Display projects filtered by category with search, status filtering, and sorting."""
    category = get_object_or_404(ProjectCategory, slug=slug)
    projects = Project.objects.filter(category=category).select_related('category').prefetch_related('images')

    # Search functionality
    search_query = request.GET.get('q', '').strip()
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(detailed_description__icontains=search_query)
        )

    # Filter by status
    selected_status = request.GET.get('status', '').strip()
    if selected_status and selected_status in ['planned', 'ongoing', 'completed', 'suspended']:
        projects = projects.filter(status=selected_status)

    # Sorting
    sort_by = request.GET.get('sort', '-is_featured')
    valid_sort_options = ['-is_featured', '-start_date', 'start_date', '-budget', 'budget', 'title', '-title']
    if sort_by in valid_sort_options:
        if sort_by == '-is_featured':
            projects = projects.order_by('-is_featured', 'order', '-start_date')
        else:
            projects = projects.order_by(sort_by)
    else:
        projects = projects.order_by('-is_featured', 'order', '-start_date')

    # Get categories with project counts
    categories = ProjectCategory.objects.annotate(
        project_count=Count('projects')
    ).order_by('order', 'name')

    # Get status counts for this category
    status_counts = {
        'all': Project.objects.filter(category=category).count(),
        'planned': Project.objects.filter(category=category, status='planned').count(),
        'ongoing': Project.objects.filter(category=category, status='ongoing').count(),
        'completed': Project.objects.filter(category=category, status='completed').count(),
        'suspended': Project.objects.filter(category=category, status='suspended').count(),
    }

    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'projects': page_obj,
        'categories': categories,
        'selected_category': category,
        'selected_status': selected_status,
        'search_query': search_query,
        'sort_by': sort_by,
        'status_counts': status_counts,
        'total_count': paginator.count,
    }
    return render(request, 'projects/category.html', context)
