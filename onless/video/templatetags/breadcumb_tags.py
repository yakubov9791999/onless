from django import template
from user.models import *
from video.models import *

register = template.Library()


@register.simple_tag()
def category_breadcumb():
    categories = Category.objects.all()
    return categories

