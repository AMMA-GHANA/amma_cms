from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project, ProjectCategory


def project_list(request):
    """Display list of projects with pagination."""
    projects = Project.objects.prefetch_related('images').order_by('-is_featured', 'order', '-start_date')

    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)

    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'projects': page_obj,
        'categories': ProjectCategory.objects.all(),
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
    """Display projects filtered by category."""
    category = get_object_or_404(ProjectCategory, slug=slug)
    projects = Project.objects.filter(
        category=category
    ).prefetch_related('images').order_by('-is_featured', 'order', '-start_date')

    # Pagination
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'projects': page_obj,
        'categories': ProjectCategory.objects.all(),
    }
    return render(request, 'projects/category.html', context)
