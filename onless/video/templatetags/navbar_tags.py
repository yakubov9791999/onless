from django import template
from user.models import *
from video.models import *

register = template.Library()


@register.simple_tag()
def get_mainsection():
    return MainSection.objects.all()
