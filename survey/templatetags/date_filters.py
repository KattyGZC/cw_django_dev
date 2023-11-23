from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='is_today')
def is_today(value):
    if value is None:
        return False
    return value == timezone.now().date()