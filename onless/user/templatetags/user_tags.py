from django import template
from django.shortcuts import get_object_or_404

from user.models import *
from video.models import *

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

@register.simple_tag()
def get_teacher_group(teacher_id):
    teacher = User.objects.get(id=teacher_id)
    groups = Group.objects.filter(teacher=teacher)
    return {
        'groups': groups
    }

@register.simple_tag()
def get_view(user_id, video_id):
    pupil = get_object_or_404(User, id=user_id)
    video = get_object_or_404(Video, id=video_id)
    views = ViewComplete.objects.filter(user=pupil, video=video)
    for view in views:
        return view

@register.simple_tag()
def get_fullname_group(group_id):
    group = get_object_or_404(Group, id=group_id)
    group_name = str(f'{group.category}-{group.number} {group.year}')
    return group_name

@register.simple_tag()
def get_pupil_attendance(pupil_id, subject_id, teacher_id):
    pupil = get_object_or_404(User, id=pupil_id)
    teacher = get_object_or_404(User, id=teacher_id)
    subject = get_object_or_404(Subject, id=subject_id)
    today = timezone.now()

    attendance = Attendance.objects.filter(pupil=pupil, teacher=teacher, subject=subject,created_date__day=today.day)
    if attendance.exists():
        for atten in attendance:
            if atten.is_visited == True:
                return True
            else:
                return False


@register.filter
def get_offline_pupils(users):
    print(users.filter(is_offline=True).count())
    return str(users.filter(is_offline=True).count())