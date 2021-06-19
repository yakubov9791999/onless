from django import template
from user.models import *
from video.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def category_breadcumb(context):
    request = context['request']
    category_id = request.get_full_path().split('/')[-1]
    category = Category.objects.get(id=category_id)
    return category

