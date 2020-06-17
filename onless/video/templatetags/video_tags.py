from django import template

from user.models import *
from video.models import *

register = template.Library()

@register.simple_tag
def get_view_video(user_id, video_id):
    user = User.objects.get(id=user_id)
    video = Video.objects.get(id=video_id)
    view_this_video = ViewComplete.objects.filter(user=user, video=video)
    return view_this_video