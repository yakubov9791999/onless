from django import template
from django.shortcuts import get_object_or_404

from sign.models import *

register = template.Library()


@register.simple_tag()
def get_file_url(file_id):
    material = get_object_or_404(Material, id=file_id)
    return material.file.url


@register.simple_tag()
def get_video_materials(video_id):
    video = get_object_or_404(Video, id=video_id)
    materials = Material.objects.filter(video=video, is_active=True)
    return materials


@register.simple_tag()
def count_materials(school_id):
    school = get_object_or_404(School, id=school_id)
    materials = Material.objects.filter(is_active=True,school=school).count()
    return materials

@register.simple_tag()
def view_sign(queryset):
    return queryset.objects.all().order_by('sort')