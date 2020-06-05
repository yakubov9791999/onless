from django import template

from user.models import *
from video.models import *

register = template.Library()

@register.simple_tag
def get_videos():
    return Video.objects.all()


@register.simple_tag
def get_group():
    return Group.objects.all()