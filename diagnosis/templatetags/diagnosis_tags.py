from django import template

register = template.Library()


@register.filter
def confidence_color(value):
    """Returns CSS class based on confidence percentage."""
    try:
        val = float(value)
        if val >= 80:
            return 'confidence-high'
        elif val >= 50:
            return 'confidence-medium'
        return 'confidence-low'
    except (ValueError, TypeError):
        return 'confidence-low'


@register.filter
def percentage_bar_width(value):
    """Returns width style for confidence bars."""
    try:
        return f"width: {min(float(value), 100)}%"
    except (ValueError, TypeError):
        return "width: 0%"
