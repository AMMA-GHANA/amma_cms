"""Forms for staff portal"""

from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from apps.news.models import NewsArticle, NewsCategory


class CKEditor5WidgetNoRequired(CKEditor5Widget):
    """Custom CKEditor5Widget that doesn't add required attribute to prevent browser validation issues"""

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        # Remove required attribute to prevent "invalid form control not focusable" error
        attrs.pop('required', None)
        return attrs


class NewsArticleForm(forms.ModelForm):
    """Form for creating and editing news articles"""

    class Meta:
        model = NewsArticle
        fields = [
            'title',
            'slug',
            'excerpt',
            'content',
            'category',
            'featured_image',
            'image_caption',
            'status',
            'is_featured',
            'published_date',
            'meta_description',
        ]
        widgets = {
            'content': CKEditor5WidgetNoRequired(
                attrs={'class': 'django_ckeditor_5'},
                config_name='default'
            ),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Enter article title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'auto-generated-from-title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'rows': 3,
                'maxlength': 300,
                'placeholder': 'Brief summary (max 300 characters)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'accept': 'image/*'
            }),
            'image_caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Optional caption'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-amma-gold focus:ring-amma-gold'
            }),
            'published_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'type': 'datetime-local'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'rows': 2,
                'maxlength': 160,
                'placeholder': 'SEO description (max 160 characters)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make slug optional (will be auto-generated)
        self.fields['slug'].required = False
        # Make featured_image optional for edits
        self.fields['featured_image'].required = False

    def clean_content(self):
        """Custom validation for content field"""
        content = self.cleaned_data.get('content', '')

        # Check if content is empty or contains only empty HTML tags
        if not content or not content.strip():
            raise forms.ValidationError('Content is required.')

        # Check for essentially empty content (just empty tags)
        import re
        # Remove all HTML tags and check if there's any actual content
        text_only = re.sub(r'<[^>]+>', '', content)
        if not text_only.strip():
            raise forms.ValidationError('Content cannot be empty.')

        return content
