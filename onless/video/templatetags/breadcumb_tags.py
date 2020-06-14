from django import template
from user.models import *
from video.models import *

register = template.Library()


# @register.inclusion_tag('inc/breadcumb.html')
# def category_breadcumb(category):
#     return {
#         'category': category
#     }

