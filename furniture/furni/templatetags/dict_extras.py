# furni/templatetags/dict_extras.py

from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    """Safely get a value from a dictionary by key."""
    if d and isinstance(d, dict):
        return d.get(key, 'N/A')  # You can change 'N/A' to anything you want
    return 'N/A'

@register.filter
def percentage(num,count):
    try:
        return int((num/count) * 100)
    except (ValueError, TypeError):
        return ''
