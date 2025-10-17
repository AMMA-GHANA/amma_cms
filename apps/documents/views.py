from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Count, Q, F
from .models import Document, DocumentCategory


def document_list(request):
    """Display list of public documents with pagination, filtering, search and sorting."""
    documents = Document.objects.filter(is_public=True).select_related('category')

    # Get query parameters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    year = request.GET.get('year')
    quarter = request.GET.get('quarter')
    sort_by = request.GET.get('sort', '-document_year')

    # Filter by category if provided
    selected_category = None
    if category_slug:
        documents = documents.filter(category__slug=category_slug)
        selected_category = DocumentCategory.objects.filter(slug=category_slug).first()

    # Filter by year if provided
    selected_year = None
    if year:
        try:
            selected_year = int(year)
            documents = documents.filter(document_year=selected_year)
        except ValueError:
            pass

    # Filter by quarter if provided
    selected_quarter = None
    if quarter and quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
        selected_quarter = quarter
        documents = documents.filter(document_quarter=quarter)

    # Search functionality
    if search_query:
        documents = documents.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Sorting
    valid_sorts = {
        '-document_year': '-document_year',
        'document_year': 'document_year',
        'title': 'title',
        '-title': '-title',
        '-download_count': '-download_count',
    }
    sort_by = valid_sorts.get(sort_by, '-document_year')

    # Handle null years in sorting - put them at the end
    if sort_by == '-document_year':
        documents = documents.order_by(
            F('document_year').desc(nulls_last=True),
            '-uploaded_date'
        )
    elif sort_by == 'document_year':
        documents = documents.order_by(
            F('document_year').asc(nulls_last=True),
            'uploaded_date'
        )
    else:
        documents = documents.order_by(sort_by)

    # Pagination
    paginator = Paginator(documents, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Group documents by year for display
    from collections import OrderedDict
    documents_by_year = OrderedDict()
    for doc in page_obj:
        year = doc.document_year if doc.document_year else 'No Year'
        if year not in documents_by_year:
            documents_by_year[year] = []
        documents_by_year[year].append(doc)

    # Get categories with document counts
    categories = DocumentCategory.objects.annotate(
        doc_count=Count('documents', filter=Q(documents__is_public=True))
    ).filter(doc_count__gt=0)

    # Get available years with document counts
    years = Document.objects.filter(
        is_public=True,
        document_year__isnull=False
    ).values('document_year').annotate(
        doc_count=Count('id')
    ).order_by('-document_year')

    # Available quarters
    quarters = ['Q1', 'Q2', 'Q3', 'Q4']

    context = {
        'documents': page_obj,
        'documents_by_year': documents_by_year,
        'categories': categories,
        'selected_category': selected_category,
        'years': years,
        'selected_year': selected_year,
        'quarters': quarters,
        'selected_quarter': selected_quarter,
        'search_query': search_query or '',
        'sort_by': sort_by,
        'total_count': paginator.count,
    }
    return render(request, 'documents/list.html', context)


def document_download(request, pk):
    """Handle document download and increment counter."""
    document = get_object_or_404(Document, pk=pk, is_public=True)

    # Increment download counter
    document.increment_downloads()

    try:
        return FileResponse(
            document.file.open('rb'),
            as_attachment=True,
            filename=document.file.name.split('/')[-1]
        )
    except FileNotFoundError:
        raise Http404("Document file not found")
