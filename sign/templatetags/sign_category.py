from django import template
from sign.models import *

register = template.Library()

@register.simple_tag()
def get_sign_category():
    return SignCategory.objects.all().order_by('sort')