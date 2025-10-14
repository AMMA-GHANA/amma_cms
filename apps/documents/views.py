from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404
from django.core.paginator import Paginator
from .models import Document, DocumentCategory


def document_list(request):
    """Display list of public documents with pagination."""
    documents = Document.objects.filter(is_public=True).select_related('category').order_by('-uploaded_date')

    # Filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        documents = documents.filter(category__slug=category_slug)

    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        documents = documents.filter(title__icontains=search_query)

    # Pagination
    paginator = Paginator(documents, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'documents': page_obj,
        'categories': DocumentCategory.objects.all(),
        'search_query': search_query,
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
