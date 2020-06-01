from django import template

from video.models import Video, VideoCategory

register = template.Library()

@register.simple_tag
def get_videos():
    return Video.objects.all()


@register.simple_tag
def get_category():
    return VideoCategory.objects.all()