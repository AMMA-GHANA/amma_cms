"""Forms for staff portal"""

from django import forms
from django.forms import inlineformset_factory
from django_ckeditor_5.widgets import CKEditor5Widget
from apps.news.models import NewsArticle, NewsCategory
from apps.projects.models import Project, ProjectCategory, ProjectImage


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


class ProjectForm(forms.ModelForm):
    """Form for creating and editing projects"""

    class Meta:
        model = Project
        fields = [
            'title',
            'slug',
            'description',
            'detailed_description',
            'category',
            'status',
            'location',
            'start_date',
            'completion_date',
            'budget',
            'beneficiaries',
            'impact_icon',
            'impact_text',
            'is_featured',
            'order',
        ]
        widgets = {
            'detailed_description': CKEditor5WidgetNoRequired(
                attrs={'class': 'django_ckeditor_5'},
                config_name='default'
            ),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Enter project title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'auto-generated-from-title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'rows': 3,
                'placeholder': 'Short description (used in cards and listings)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Project location/community'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'type': 'date'
            }),
            'completion_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'type': 'date'
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'beneficiaries': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'E.g., 5,000+ citizens served daily'
            }),
            'impact_icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Lucide icon name (e.g., users)'
            }),
            'impact_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Impact description for card display'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-amma-gold focus:ring-amma-gold'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': '0'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make slug optional (will be auto-generated)
        self.fields['slug'].required = False
        # Make optional fields explicit
        self.fields['detailed_description'].required = False
        self.fields['start_date'].required = False
        self.fields['completion_date'].required = False
        self.fields['budget'].required = False
        self.fields['beneficiaries'].required = False
        self.fields['impact_icon'].required = False
        self.fields['impact_text'].required = False

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        completion_date = cleaned_data.get('completion_date')

        # Validate that completion date is after start date
        if start_date and completion_date and completion_date < start_date:
            raise forms.ValidationError('Completion date must be after start date.')

        return cleaned_data


class ProjectImageForm(forms.ModelForm):
    """Form for project images"""

    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'is_primary', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent',
                'placeholder': 'Optional caption'
            }),
            'is_primary': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-amma-gold focus:ring-amma-gold'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amma-gold focus:border-transparent'
            }),
        }


# Formset for managing multiple project images
ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    form=ProjectImageForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False
)
