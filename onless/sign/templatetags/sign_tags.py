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

@register.simple_tag()
def check_schedule_disable_or_enable(group_id,theme_id):
    group = get_object_or_404(Group, id=group_id)
    theme = get_object_or_404(Theme, id=theme_id)

    if theme.theme_order == None:
        schedule = Schedule.objects.filter(group=group,  theme=theme, sort=theme.sort)
    else:
        schedule = Schedule.objects.filter(group=group,  theme=theme, sort=theme.sort, theme_order=theme.theme_order)

    if schedule.exists():
        return True
    else:
        return False
