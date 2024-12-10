from django import template

register = template.Library()

@register.filter
def range_filter(value):
    """Generate a range for Django templates."""
    return range(value)
