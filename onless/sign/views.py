import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, IntegerField
from django.db.models.functions import Cast
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from datetime import datetime as dt, timedelta

from django.utils import formats

from sign.decorators import *
from user.decorators import *
from sign.forms import *
from sign.models import *
from video.models import Category


@login_required
def sign(request):
    categories = SignCategory.objects.all()
    signs = Sign.objects.all()
    return render(request, 'sign/signs.html', {
        'signs': signs,
        'categories': categories,
    })


# @login_required
# def traffic_rules(request):
#     traffic_rules = TrafficRules.objects.all()
#     return render(request, 'sign/traffic_rules.html', {
#         'traffic_rules': traffic_rules,
#         # 'categories': categories,
#     })

@login_required
def schedules_list(request):
    school = get_object_or_404(School, id=request.user.school.id)
    teachers = User.objects.filter(Q(is_active=True) & Q(school=school) & Q(Q(role=3) | Q(role=2)))
    if not teachers.exists():
        messages.error(request, 'O\'qituvchilar mavjud emas!')
    context = {
        'teachers': teachers
    }
    if request.user.role == '3':
        groups = Group.objects.filter(Q(is_active=True) & Q(school=school) & Q(teacher=request.user)).order_by('-id')
        context.update(groups=groups)
        context.update(group=groups[0])
        context.update(teacher=groups[0].teacher)
        if not groups.exists():
            messages.error(request, 'Siz rahbarlik qilayotgan guruhlar mavjud emas!')
    if request.user.role == '2':
        groups = Group.objects.filter(Q(is_active=True) & Q(school=school)).order_by('-id')
        context.update(groups=groups)
        context.update(group=groups[0])
        context.update(teacher=groups[0].teacher)
        if not groups.exists():
            messages.error(request, 'Sizda guruhlar mavjud emas!')
    themes = Theme.objects.filter(
        Q(is_active=True) & Q(category__title=context.get('group').category)).order_by("sort")
    context.update(themes=themes)
    if request.POST:
        group = get_object_or_404(Group, id=request.POST.get('group'))
        themes = Theme.objects.filter(Q(is_active=True) & Q(category__title=group.category)).order_by("sort")
        context.update(group=group)
        context.update(themes=themes)
        return render(request, 'sign/schedules_list.html', context)
    return render(request, 'sign/schedules_list.html', context)


@login_required
def save_schedule(request):
    if request.is_ajax():
        if request.POST:
            if request.POST.getlist('schedules[]'):
                schedules = request.POST.getlist('schedules[]')
                groupd_id = request.POST.getlist('group')
                groupd_id = str(groupd_id).replace('[', '').replace(']', '').replace('"', '').replace("'", '')
                group = get_object_or_404(Group, id=groupd_id)
                date = schedules[0]
                lesson_time = schedules[1]
                theme_id = schedules[2]
                teacher_id = schedules[3]
                theme_order = schedules[4]
                date = datetime.datetime.strptime(date, '%d.%m.%Y').date()
                theme = get_object_or_404(Theme, id=theme_id)
                teacher = get_object_or_404(User, id=teacher_id)
                print(teacher)
                schedules = Schedule.objects.filter(group=group, theme=theme,sort=theme.sort, theme_order=theme_order)
                if schedules.exists():
                    for schedule in schedules:
                        schedule.lesson_time = lesson_time
                        schedule.teacher = teacher
                        schedule.author = request.user
                        schedule.date = date
                        schedule.updated_date = timezone.now()
                        schedule.save()
                else:
                    schedule = Schedule.objects.create(date=date, theme_order=theme_order, sort=theme.sort)
                    schedule.lesson_time = lesson_time
                    schedule.theme = theme
                    schedule.teacher = teacher
                    if theme.subject:
                        schedule.subject = get_object_or_404(Subject, id=theme.subject.id)
                    schedule.author = request.user
                    schedule.group = group
                    schedule.save()

                return HttpResponse(True)
            else:
                return HttpResponse(False)
        else:
            return HttpResponse(False)
    return HttpResponse(False)


# @login_required
# def add_subject(request):
#     if request.POST:
#         form = AddSubjectForm(request.POST)
#         author = User.objects.get(id=request.user.id)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.author = author
#             form.created_date = timezone.now()
#             form.school_id = request.user.school.id
#             form.save()
#             messages.success(request, "Muvaffaqiyatli qo'shildi !")
#         else:
#             messages.error(request, "Formani to'ldirishda xatolik !")
#     return render(request, 'sign/add_subject.html',)


@login_required
def update_schedule(request, id):
    if request.user.role == '3':
        groups = Group.objects.filter(Q(is_active=True) & Q(school=request.user.school) & Q(teacher=request.user))
        if not groups.exists():
            messages.error(request, 'Siz rahbarlik qilayotgan guruhlar mavjud emas!')
            return render(request, 'sign/old_schedules_list.html', {'groups': groups})
    else:
        groups = Group.objects.filter(Q(is_active=True) & Q(school=request.user.school))
        if not groups.exists():
            messages.error(request, 'Sizda guruhlar mavjud emas!')
            return render(request, 'sign/old_schedules_list.html')
    schedule = Schedule.objects.get(id=id)
    context = {
        'schedule': schedule,
        'groups': groups
    }

    if schedule.group.school.director == request.user or schedule.group.teacher == request.user:
        if request.POST:
            get_date = request.POST.get('date').split('.')
            date = f'{get_date[2]}-{get_date[1]}-{get_date[0]}'
            form = UpdateScheduleForm(request.POST, instance=schedule)
            if form.is_valid():
                form = form.save(commit=False)
                form.date = date
                form.start = request.POST.get('start')
                form.stop = request.POST.get('stop')
                form.updated_date = timezone.now()
                form.schedule = schedule
                form.save()
                messages.success(request, "Muvaffaqiyatli tahrirlandi !")
                return render(request, 'sign/old_schedules_list.html', context)
            else:
                messages.error(request, "Formani to'ldirishda xatolik !")
        else:
            return render(request, 'sign/update_schedule.html', context)
        return render(request, 'sign/update_schedule.html', context)
    else:
        groups = Group.objects.filter(Q(is_active=True) & Q(school=request.user.school))
        context.update(groups=groups)
        messages.error(request, 'Mavzuni tahrirlash guruh rahbari va maktab rahbariga ruxsat berilgan!')
        return render(request, 'sign/old_schedules_list.html', context)


# @login_required
# def update_subject(request, id):
#     subject = get_object_or_404(Subject, id=id)
#     context = {
#         'subject': subject
#     }
#     if request.POST:
#         form = UpdateSubjectForm(request.POST, instance=subject)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.author = request.user
#             form.updated_date = timezone.now()
#             form.save()
#             messages.success(request, "Muvaffaqiyatli tahrirlandi !")
#             return render(request, 'sign/update_subject.html', context)
#         else:
#             messages.error(request, "Formani to'ldirishda xatolik !")
#             return render(request, 'sign/update_subject.html', context)
#     return render(request, 'sign/update_subject.html',context)


@login_required
def delete_schedule(request, id):
    groups = Group.objects.filter(Q(is_active=True) & Q(school=request.user.school))
    if not groups.exists():
        messages.error(request, 'Sizda guruhlar mavjud emas!')
    schedule = Schedule.objects.get(id=id)
    context = {
        'schedule': schedule,
        'groups': groups
    }

    if schedule.group.school.director == request.user or schedule.group.teacher == request.user:
        schedule.delete()
        return render(request, 'sign/old_schedules_list.html', context)
    else:
        messages.error(request, 'Mavzuni o\'chirish guruh rahbari va maktab rahbariga ruxsat berilgan!')
        return render(request, 'sign/old_schedules_list.html', context)


@login_required
def subjects_list(request):
    subjects = Subject.objects.filter(Q(is_active=True))
    if not subjects.exists():
        messages.error(request, 'Fanlar mavjud emas!')
    context = {
        'subjects': subjects
    }
    if request.user.role == '4':
        subjects = Subject.objects.filter(Q(is_active=True) & Q(categories__title=request.user.group.category))
        if not subjects.exists():
            messages.error(request, 'Fanlar mavjud emas!')
        context.update(subjects=subjects)
    return render(request, 'sign/subjects_list.html', context)


@login_required
def get_subject(request):
    if request.is_ajax():
        group = get_object_or_404(Group, id=request.GET.get('group'))
        subjects = Subject.objects.filter(Q(is_active=True) & Q(categories__title=group.category))
        options = "<option>-- -- --</option>"
        for subject in subjects:
            options += f"<option value='{subject.id}'>{subject.short_title} - {subject.long_title}</option>"
        return HttpResponse(options)
    else:
        return False


@login_required
def get_subject_long_title(request):
    if request.is_ajax():
        subject = get_object_or_404(Subject, id=request.GET.get('subject'))
        return HttpResponse(subject.long_title)
    else:
        return False


@login_required
def group_subjects(request):
    if request.is_ajax():
        group = get_object_or_404(Group, id=request.GET.get('group'))
        subjects = Subject.objects.filter(Q(is_active=True) & Q(categories__title=group.category)).distinct()

        if subjects.exists():
            options = "<option>-- -- --</option>"
            for subject in subjects:
                options += f"<option value='{subject.id}'>{subject.short_title} - {subject.long_title}</option>"
            return HttpResponse(options)
        else:
            return HttpResponse(False)
    else:
        return False


@login_required
def get_schedule(request):
    if request.is_ajax():
        group = get_object_or_404(Group, id=request.GET.get('group'))
        schedules = Schedule.objects.filter(subject=request.GET.get('subject'), group=group)

        td = ""

        for schedule in schedules:
            url_update = reverse_lazy('sign:update_schedule', kwargs={'id': schedule.id})
            url_delete = reverse_lazy('sign:delete_schedule', kwargs={'id': schedule.id})

            td += f"<tr>" \
                  f"<td>M-{schedule.sort}</td>" \
                  f"<td class='schedule_title'>{schedule.theme}</td>" \
                  f"<td>{schedule.date.strftime('%d.%m.%Y')}</td>" \
                  f"<td>{str(schedule.start)[0:16]}</td>" \
                  f"<td>{str(schedule.stop)[0:16]}</td>" \
                  f"<td class='edit_block'><a href='{url_update}'><button class='btn btn-primary'><i class='fa fa-edit'></i></button></a>&nbsp<a class='deleteBtn' data-title='{schedule.theme}' data-id='{schedule.id}' href='#'><button class='btn btn-danger'><i class='fa fa-trash'></i></button></a></td>" \
                  f"</tr>"
        return HttpResponse(td)
    else:
        return False


@login_required
def materials(request):
    materials = Material.objects.filter(is_active=True).order_by('-id')

    context = {
        'materials': materials
    }

    return render(request, "sign/materials.html", context)


@login_required
def add_material(request):
    if request.user.role == '2' or request.user.role == '3':
        categories = Category.objects.filter(is_active=True)
        context = {
            'categories': categories
        }
        if request.POST and request.FILES:
            form = AddMaterialFrom(request.POST or None, request.FILES or None)
            if form.is_valid():
                title = form.cleaned_data['title']
                title = get_title(title)
                file = request.FILES['file']
                ext = os.path.splitext(file.name)[1]
                title = os.path.splitext(title)[0]
                if file.size < 25242880:
                    form = form.save(commit=False)
                    form.title = '{}{}'.format(title, ext)
                    form.school = request.user.school
                    if request.POST['video'] != 'False':
                        video = get_object_or_404(Video, id=request.POST['video'])
                        form.video = video
                    form.author = request.user
                    form.save()
                    messages.success(request, "Muvaffaqiyatli qo'shildi !")
                else:
                    messages.error(request, "Fayl hajmi 25 mb dan ortiq bo'lmasligi kerak !")
        else:
            form = AddMaterialFrom()
        context.update(form=form)

        return render(request, "sign/add_material.html", context)
    else:
        return render(request, 'inc/404.html')


@login_required
def get_video(request):
    if request.is_ajax():
        category = get_object_or_404(Category, id=request.GET.get('category'))
        videos = Video.objects.filter(is_active=True, category=category)
        options = "<option value='False'>--- --- ---</option>"
        for video in videos:
            options += f"<option value='{video.id}'>{video.title}</option>"
        return HttpResponse(options)
    else:
        return False


@login_required
def delete_material(request, id):
    material = get_object_or_404(Material, id=id)
    if material.author == request.user:
        material.is_active = False
        material.save()
    else:
        return render(request, 'inc/404.html')

# @login_required
# def get_group_full_schedule(request):
#     if request.is_ajax():
#         group = get_object_or_404(Group, id=request.GET.get('group'))
#         schedules = Schedule.objects.filter(Q(is_active=True)).distinct()
#         print(schedules)
#
#         if schedules.exists():
#             options = "<option>-- -- --</option>"
#             for subject in schedules:
#                 options += f"<option value='{subject.id}'>{subject.theme}</option>"
#             return HttpResponse(options)
#         else:
#             return HttpResponse(False)
#     else:
#         return False
