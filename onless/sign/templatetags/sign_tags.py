from datetime import timedelta

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
def count_schedules(school_id):
    school = get_object_or_404(School, id=school_id)
    schedules = Schedule.objects.filter(is_active=True,author__school=school).count()
    return schedules

@register.filter
def view_sign(queryset):
    return queryset.order_by('sort')

@register.filter
def daterange(start_date, end_date):
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=5)
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)