from django import template
from django.shortcuts import get_object_or_404

from user.models import *

register = template.Library()


@register.simple_tag()
def get_count(school_id):
    school = School.objects.get(id=school_id)
    pupils = User.objects.filter(school=school, role=4).count()
    teachers = User.objects.filter(school=school, role=3).count()
    groups = Group.objects.filter(school=school).count()
    bugalters = User.objects.filter(school=school, role=5).count()
    return {
        'pupils': pupils,
        'teachers': teachers,
        'groups': groups,
        'bugalters': bugalters
    }

@register.simple_tag()
def get_payments(pupil_id, group_id):
    pupil = get_object_or_404(User, id=pupil_id)
    group = get_object_or_404(Group, id=group_id)
    values = Pay.objects.filter(pupil=pupil)
    total = group.price
    payment = 0
    debit = 0
    for value in values:
        payment += value.payment
    debit = group.price - payment
    return  {
            'payment': payment,
            'total': total,
            'debit': debit,
            'values': values
        }

