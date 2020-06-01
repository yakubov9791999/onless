from django import template

from video.models import Video, Category

register = template.Library()

@register.simple_tag
def get_videos():
    return Video.objects.all()


@register.simple_tag
def get_category():
    return Category.objects.all()