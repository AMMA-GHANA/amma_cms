from django import template
import json
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def tojson(value):
    """Convert Python object to JSON string for use in JavaScript"""
    # Handle None and empty values
    if value is None:
        return mark_safe('null')
    return mark_safe(json.dumps(value))
