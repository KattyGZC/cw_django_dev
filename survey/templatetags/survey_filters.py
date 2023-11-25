from django import template
from django.utils import timezone

from survey.models import Answer

register = template.Library()

@register.filter(name='is_today')
def is_today(value):
    if value is None:
        return False
    return value == timezone.now().date()

@register.filter(name='check_user_answer')
def check_user_answer(question, user):
    if not user.is_authenticated:
        return None
    answer = Answer.objects.filter(question=question, author=user).first()
    return str(answer.value) if answer else None