from django.shortcuts import render
from .models import HeroSlide, Statistic, AboutSection
from apps.services.models import Service
from apps.news.models import NewsArticle
from apps.projects.models import Project
from apps.staff.models import StaffMember


def homepage(request):
    """
    Homepage view with all dynamic content sections.

    Displays:
    - Hero carousel slides
    - Statistics counters
    - About section
    - Featured services
    - Featured news articles
    - Featured projects
    - Leadership team
    """
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True).order_by('order')[:8],
        'statistics': Statistic.objects.filter(is_active=True).order_by('order')[:4],
        'about_section': AboutSection.load(),
        'services': Service.objects.filter(is_active=True).order_by('order')[:6],
        'featured_news': NewsArticle.objects.filter(
            status='published',
            is_featured=True
        ).select_related('category', 'author').order_by('-published_date')[:3],
        'featured_projects': Project.objects.filter(
            is_featured=True
        ).prefetch_related('images').order_by('order')[:3],
        'leadership': StaffMember.objects.filter(
            position_type__in=['leadership', 'management'],
            is_active=True
        ).select_related('department').order_by('display_order')[:6]
    }
    return render(request, 'core/homepage.html', context)


def about_page(request):
    """About page view."""
    context = {
        'about_section': AboutSection.load(),
        'statistics': Statistic.objects.filter(is_active=True).order_by('order'),
    }
    return render(request, 'core/about.html', context)
