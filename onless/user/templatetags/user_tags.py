from django import template
from django.shortcuts import get_object_or_404

from user.models import *
from video.models import *

register = template.Library()


@register.simple_tag()
def get_count(school_id):
    school = School.objects.get(id=school_id)
    pupils = User.objects.filter(is_active=True, school=school, role=4).count()
    teachers = User.objects.filter(is_active=True, school=school, role=3).count()
    groups = Group.objects.filter(is_active=True, school=school).count()
    bugalters = User.objects.filter( is_active=True,school=school, role=5).count()
    instructors = User.objects.filter(is_active=True, school=school, role=6).count()
    return {
        'pupils': pupils,
        'teachers': teachers,
        'groups': groups,
        'bugalters': bugalters,
        'instructors': instructors
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
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    attendance = Attendance.objects.filter(pupil=pupil, teacher=teacher, subject=subject,created_date__range=(today_min, today_max))
    if attendance.exists():
        for atten in attendance:
            if atten.is_visited == True:
                return True
            elif atten.is_visited == False:
                return False

@register.simple_tag()
def get_pupil_attendance_time(pupil_id, subject_id):
    pupil = get_object_or_404(User, id=pupil_id)
    subject = get_object_or_404(Subject, id=subject_id)

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

    attendance = Attendance.objects.filter(pupil=pupil, subject=subject,
                                           created_date__range=(today_min, today_max))
    if attendance.exists():
        for atten in attendance:
            return atten.updated_date


@register.filter
def get_offline_pupils(users):
    return str(users.filter(is_offline=True).count())


@register.simple_tag()
def get_group_pay(group_id):
    group = Group.objects.get(id=group_id)
    pupils = User.objects.filter(role='4', group=group, is_active=True)
    total_pay = group.price * pupils.count()
    pays = Pay.objects.filter(pupil__in=pupils)
    payment = 0
    for pay in pays:
        payment += int(pay.payment)
    debit = total_pay - payment

    return {
        'payment': payment,
        'debit': debit,
        'total_pay': total_pay
    }