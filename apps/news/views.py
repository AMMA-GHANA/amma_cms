from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import NewsArticle, NewsCategory


def news_list(request):
    """Display list of published news articles with search, filtering, and sorting."""
    articles = NewsArticle.objects.filter(
        status='published'
    ).select_related('category', 'author')

    # Get query parameters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    year = request.GET.get('year')
    sort_by = request.GET.get('sort', '-published_date')

    # Filter by category if provided
    selected_category = None
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
        selected_category = NewsCategory.objects.filter(slug=category_slug).first()

    # Filter by year if provided
    selected_year = None
    if year:
        try:
            selected_year = int(year)
            articles = articles.filter(published_date__year=selected_year)
        except ValueError:
            pass

    # Search functionality
    if search_query:
        articles = articles.filter(
            Q(title__icontains=search_query) |
            Q(excerpt__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Sorting
    valid_sorts = {
        '-published_date': '-published_date',
        'published_date': 'published_date',
    }
    sort_by = valid_sorts.get(sort_by, '-published_date')
    articles = articles.order_by(sort_by)

    # Get featured article (first featured or first article)
    featured_article = None
    featured_articles = articles.filter(is_featured=True)[:1]
    if featured_articles:
        featured_article = featured_articles[0]
        # Exclude featured article from main list
        articles = articles.exclude(pk=featured_article.pk)
    elif articles.exists():
        featured_article = articles.first()
        articles = articles.exclude(pk=featured_article.pk)

    # Pagination
    paginator = Paginator(articles, 11)  # 11 because 1 is featured
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get categories with article counts
    categories = NewsCategory.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('name')

    # Get available years with article counts
    years = NewsArticle.objects.filter(
        status='published',
        published_date__isnull=False
    ).dates('published_date', 'year', order='DESC')

    # Get most viewed articles for sidebar
    most_viewed = NewsArticle.objects.filter(
        status='published'
    ).order_by('-views')[:5]

    context = {
        'articles': page_obj,
        'featured_article': featured_article,
        'categories': categories,
        'selected_category': selected_category,
        'years': years,
        'selected_year': selected_year,
        'search_query': search_query or '',
        'sort_by': sort_by,
        'total_count': paginator.count + (1 if featured_article else 0),
        'most_viewed': most_viewed,
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
