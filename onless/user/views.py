import random
from random import randrange

import requests
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView

from .forms import *
from user.models import User, Group, CATEGORY_CHOICES, School
from video.views import *

from django.db import IntegrityError


#
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/home/')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
            return HttpResponseRedirect('/accounts/login/')


@login_required
def add_list(request):
    if request.user.role == '2' or request.user.role == '3':
        return render(request, 'user/add_list.html')
    else:
        return render(request, 'inc/404.html')


@login_required
def settings_list(request):
    return render(request, 'user/settings_list.html')


@login_required
def add_teacher(request):
    if request.user.role == '2' or request.user.role == '3':
        if request.method == 'POST':
            form = AddUserForm(data=request.POST)
            password = random.randint(1000000, 9999999)
            if form.is_valid():
                try:
                    user = User.objects.create_user(
                        username=request.POST['pasport'],
                        pasport = request.POST['pasport'],
                        school=request.user.school,
                        turbo=password,
                        password=password,
                        name=form.cleaned_data['name'],
                        phone=form.cleaned_data['phone'],
                        role='3',
                        is_superuser=False,
                    )
                    user.set_password(password)
                    user.username = request.POST['pasport']
                    user.email = ''
                    user.save()

                    messages.success(request, "O'qituvchi muvaffaqiyatli qo'shildi")
                except IntegrityError:
                    messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
            else:
                messages.error(request, "Formani to'liq to'ldiring !")
        else:
            form = AddUserForm(request)
        return render(request, 'user/add_teacher.html', )
    else:
        return render(request, 'inc/404.html')


@login_required
def add_pupil(request):
    if request.user.role == '2' or request.user.role == '3':
        groups = Group.objects.all()

        context = {
            'groups': groups,

        }
        form = AddUserForm()
        context = {
            'groups': groups,
            'form': form,
        }
        if request.method == 'POST':
            form = AddUserForm(data=request.POST)
            group = Group.objects.get(id=request.POST['group'])
            parol = random.randint(1000000, 9999999)
            if form.is_valid():
                try:
                    user = User.objects.create_user(
                        username=request.POST['pasport'],
                        school=request.user.school,
                        turbo=parol,
                        password=parol,
                        name=form.cleaned_data['name'],
                        phone=form.cleaned_data['phone'],
                        role='4',
                        group=group,
                        is_superuser=False,
                    )
                    user.set_password(parol)
                    user.username = request.POST['pasport']
                    user.email = ''
                    user.save()
                    msg = f"Hurmatli {user.name}! Siz {user.group.category}-{user.group.number} guruhiga onlayn o'qish rejimida qabul qilindingiz. Darslarga qatnashish uchun http://onless.uz manziliga kiring. %0aLogin: {user.username}%0aParol: {user.turbo}%0aQo'shimcha savollar bo'lsa {user.school.phone} raqamiga qo'ng'iroq qilishingiz mumkin"
                    msg = msg.replace(" ", "+")
                    url = f"https://developer.apix.uz/index.php?app=ws&u={request.user.school.sms_login}&h={request.user.school.sms_token }&op=pv&to=998{user.phone}&unicode=1&msg={msg}"
                    response = requests.get(url)

                    messages.success(request, "O'quvchi muvaffaqiyatli qo'shildi")
                except IntegrityError:
                    messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
            else:
                messages.error(request, "Formani to'liq to'ldiring !")
        else:
            form = AddUserForm()
        return render(request, 'user/add_pupil.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def add_group(request):
    if request.user.role == '2' or request.user.role == '3':
        teachers = User.objects.filter(role=3)
        context = {
            'teachers': teachers,
        }
        if request.POST:
            form = AddGroupForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                category = request.POST['category']
                teacher = form.cleaned_data['teacher']
                form = form.save(commit=False)
                form.number = number
                form.category = category
                form.teacher = teacher
                form.school = request.user.school
                form.start = request.POST['start']
                form.stop = request.POST['stop']
                form.save()
                messages.success(request, "Guruh qo'shildi")
        else:
            form = AddGroupForm()
        return render(request, 'user/add_group.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def groups_list(request):
    if request.user.role == '2' or request.user.role == '3' or request.user.role == '4':
        groups = Group.objects.filter(school=request.user.school, is_active=True)
        context = {
            'groups': groups,
        }
        return render(request, 'user/groups_list.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def group_detail(request, id):
    if request.user.role == '2' or request.user.role == '3':
        group = Group.objects.get(id=id)
        pupils = User.objects.filter(role=4, group=group)
        for pupil in pupils:
            test_answers = ResultQuiz.objects.filter(user=pupil)
            print(test_answers)

        context = {
            'group': group,
            'pupils': pupils,
        }
        return render(request, 'user/group_detail.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def group_delete(request, id):
    if request.user.role == '2' or request.user.role == '3':
        group = Group.objects.get(id=id)
        if group.group_user.count() > 2:
            group.is_active = False
            group.save()
        else:
            print('else')
            group.delete()
        return redirect(groups_list)
    else:
        return render(request, 'inc/404.html')


@login_required
def group_update(request, id):
    if request.user.role == '2' or request.user.role == '3':
        group = Group.objects.get(id=id)
        form = GroupUpdateForm(instance=group)
        context = {
            'form': form,
            'group': group,
        }
        return render(request, 'user/group_update.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def profil_edit(request):
    user = get_object_or_404(User, id=request.user.id)
    form = EditUserForm(instance=user)
    if request.POST:
        form = EditUserForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
        else:
            messages.error(request, "Formani to'ldiring !")
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'user/profil_edit.html', context)


@login_required
def school_edit(request):
    if request.user.role == '2' or request.user.role == '3':
        school = School.objects.get(id=request.user.school.id)
        form = EditSchoolForm(instance=request.user.school)
        if request.POST:
            form = EditSchoolForm(request.POST or None, request.FILES or None, instance=request.user.school)
            if form.is_valid():
                form.save()
                messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
            else:
                messages.success(request, "Formani to'ldirishda xatolik !")
        else:
            form = EditSchoolForm(instance=request.user.school)
        context = {
            'form': form
        }
        return render(request, 'user/school_edit.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def contact(request):
    if request.POST or None:
        form = AddContactForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            photo = request.POST['photo']
            form = form.save(commit=False)
            form.photo = photo
            form.save()
            messages.success(request, "Muvaffaqiyatli jo'natildi !")
        else:
            messages.error(request, "Formani to'ldiring !")
    else:
        form = AddContactForm()
    return render(request, 'user/contact.html')


@login_required
def search(request):
    query = request.GET.get('q', False).lower()

    context = {
        'q': query,
    }
    results = list()
    count = 0
    if query:
        try:
            teachers = User.objects.filter(role=3, name__contains=query, school=request.user.school)
            context.update(teachers=teachers)
            results.append(teachers)
            count += teachers.count()
        except ValueError:
            pass

        try:
            pupils = User.objects.filter(role=2, name__contains=query, school=request.user.school)
            context.update(pupils=pupils)
            results.append(pupils)
            count += pupils.count()
        except ValueError:
            pass

        try:
            groups = Group.objects.filter(
                Q(category__icontains=query) |
                Q(number=int(query)) |
                Q(year=int(query))
            ).filter(school=request.user.school)
            context.update(groups=groups)
            results.append(groups)
            count += groups.count()
        except ValueError:
            pass

        try:
            videos = Video.objects.filter(
                title__contains=query
            ).distinct()
            results.append(videos)
            context.update(videos=videos)
            count += videos.count()
        except ValueError:
            pass

        context.update(count=count)
        context.update(results=results)
    return render(request, 'user/search_result.html', context)


@login_required
def add_school(request):
    return render(request, 'user/add_school.html')


@login_required
def schools_list(request):
    return render(request, 'inspecion/schools_list.html')
