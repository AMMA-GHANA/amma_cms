from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import GalleryImage, GalleryCategory


def gallery_list(request):
    """Display gallery with all images organized by category."""
    # Get featured images
    featured_images = GalleryImage.objects.filter(is_featured=True).select_related('category').order_by('order')[:12]

    # Get all categories with image count
    categories = GalleryCategory.objects.all()

    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(GalleryCategory, slug=category_slug)
        images = GalleryImage.objects.filter(category=category).order_by('-date_taken', '-uploaded_date')
    else:
        category = None
        images = GalleryImage.objects.select_related('category').order_by('-date_taken', '-uploaded_date')

    # Pagination
    paginator = Paginator(images, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'featured_images': featured_images,
        'images': page_obj,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'gallery/list.html', context)


def album_detail(request, slug):
    """Display all images in a specific category/album."""
    category = get_object_or_404(GalleryCategory, slug=slug)
    images = GalleryImage.objects.filter(category=category).order_by('order', '-date_taken')

    # Pagination
    paginator = Paginator(images, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'images': page_obj,
        'all_categories': GalleryCategory.objects.all(),
    }
    return render(request, 'gallery/album.html', context)
