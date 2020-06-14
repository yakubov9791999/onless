from django import template

from user.models import *

register = template.Library()


@register.simple_tag()
def get_count(school_id):
    school = School.objects.get(id=school_id)
    pupils = User.objects.filter(school=school, role=4).count()
    teachers = User.objects.filter(school=school, role=3).count()
    groups = Group.objects.filter(school=school).count()
    return {
        'pupils': pupils,
        'teachers': teachers,
        'groups': groups,
    }