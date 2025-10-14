from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import NewsArticle, NewsCategory


def news_list(request):
    """Display list of published news articles with pagination."""
    articles = NewsArticle.objects.filter(
        status='published'
    ).select_related('category', 'author').order_by('-published_date')

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': page_obj,
        'categories': NewsCategory.objects.all(),
    }
    return render(request, 'news/list.html', context)


def news_detail(request, slug):
    """Display single news article detail."""
    article = get_object_or_404(
        NewsArticle.objects.select_related('category', 'author'),
        slug=slug,
        status='published'
    )

    # Increment views
    article.increment_views()

    # Related articles
    related = NewsArticle.objects.filter(
        category=article.category,
        status='published'
    ).exclude(pk=article.pk).order_by('-published_date')[:3]

    context = {
        'article': article,
        'related_articles': related,
    }
    return render(request, 'news/detail.html', context)


def news_by_category(request, slug):
    """Display news articles filtered by category."""
    category = get_object_or_404(NewsCategory, slug=slug)
    articles = NewsArticle.objects.filter(
        category=category,
        status='published'
    ).select_related('author').order_by('-published_date')

    # Pagination
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'articles': page_obj,
        'categories': NewsCategory.objects.all(),
    }
    return render(request, 'news/category.html', context)
