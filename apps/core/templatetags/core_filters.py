import re
from django import template

register = template.Library()


@register.filter
def phone_digits(value):
    """
    Extract only digits from a phone number.
    Useful for WhatsApp links, tel: links, etc.
    Example: "+91 98765-43210" -> "919876543210"
    """
    if not value:
        return ""
    return re.sub(r'\D', '', str(value))


@register.filter
def phone_display(value):
    """
    Format a phone number for display.
    Keeps + at the start if present, otherwise just returns as is.
    """
    if not value:
        return ""
    return str(value)
