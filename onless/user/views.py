import random
from random import randrange

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
                return HttpResponseRedirect('/')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
            return HttpResponseRedirect('/accounts/login/')


def add_list(request):
    return render(request, 'user/add_list.html')

def settings_list(request):
    return render(request, 'user/settings_list.html')

def add_teacher(request):
    if request.method == 'POST':
        form = AddUserForm(data=request.POST)
        password = random.randint(1000000, 9999999)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=request.POST['pasport'],
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


def add_pupil(request):
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
        parol = random.randint(1000000,9999999)
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
                messages.success(request, "O'quvchi muvaffaqiyatli qo'shildi")
            except IntegrityError:
                messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
        else:
            messages.error(request, "Formani to'liq to'ldiring !")
    else:
        form = AddUserForm()
    return render(request, 'user/add_pupil.html', context)

def add_group(request):
    teachers = User.objects.filter(role=3)
    school = School.objects.get(users=request.user)
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
            form.school_id = school.id
            form.start = request.POST['start']
            form.stop = request.POST['stop']
            form.save()
            messages.success(request, "Guruh qo'shildi")
    else:
        form = AddGroupForm()
    return render(request, 'user/add_group.html', context)


def groups_list(request):
    groups = Group.objects.filter(school=request.user.school, is_active=True)
    context = {
        'groups': groups,
    }
    return render(request, 'user/groups_list.html', context)


def group_detail(request, id):
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

def group_delete(request, id):
    group = Group.objects.get(id=id)
    if group.group_user.count() > 5:
        group.is_active = False
    else:
        try:
            group.delete()
        except ProtectedError:
            messages.error(request, "Guruhni o'chirib bo'lmaydi. Guruhda o'qiydigan o'quvchilar mavjud")
    return redirect(groups_list)

def group_update(request, id):
    group = Group.objects.get(id=id)
    form = GroupUpdateForm(instance=group)
    context = {
        'form': form,
        'group': group,
    }
    return render(request, 'user/group_update.html', context)

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





def school_edit(request):
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

def search(request):
    query = request.GET.get('q', False).lower()

    context = {
        'q': query,
    }
    results = list()
    count = 0
    if query:
        try:
            teachers = User.objects.filter(role=3,name__contains=query,school=request.user.school)
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