from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from user.models import User, Group, CATEGORY_CHOICES
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
        if form.is_valid():
            if request.POST['phone']:
                try:
                    user= User.objects.create_user(
                        username=form.cleaned_data['phone'],
                        password=form.cleaned_data['phone'],
                        turbo=form.cleaned_data['phone'],
                        name=form.cleaned_data['name'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        driving_school=request.user.driving_school,
                        role='3',
                        gender=request.POST['gender'],
                        birthday=form.cleaned_data['birthday'],
                        is_superuser=False,
                    )
                    user.set_password(request.POST['phone'])
                    user.save()
                    messages.success(request, "O'qituvchi muvaffaqaiyatli qo'shildi")

                except IntegrityError:
                    messages.error(request, "Bunday loginli foydalanuvchi mavjud")
            else:
                messages.error(request, "Bu raqam allaqachon kiritilgan")
        else:
            messages.error(request, "Formani to'ldiring")
    else:
        form = AddUserForm()
    return render(request, 'user/add_teacher.html', )


def add_pupil(request):
    groups = Group.objects.all()
    context = {
        'groups': groups
    }
    form = AddUserForm()
    if request.method == 'POST':
        form = AddUserForm(data=request.POST)
        group = Group.objects.get(id=request.POST['group'])
        if form.is_valid():
            print(request.POST)
            if request.POST['phone']:
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['phone'],
                        password=form.cleaned_data['phone'],
                        turbo=form.cleaned_data['phone'],
                        name=form.cleaned_data['name'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        driving_school=request.user.driving_school,
                        role='4',
                        gender=request.POST['gender'],
                        group=group,
                        birthday=form.cleaned_data['birthday'],
                        is_superuser=False,
                    )
                    user.set_password(request.POST['phone'])
                    user.save()
                    messages.success(request, "O'qituvchi muvaffaqaiyatli qo'shildi")

                except IntegrityError:
                    messages.error(request, "Bunday loginli foydalanuvchi mavjud")
            else:
                messages.error(request, "Bu raqam allaqachon kiritilgan")
        else:
            messages.error(request, "Formani to'ldiring")
    else:
        form = AddUserForm()
    return render(request, 'user/add_pupil.html', context )

def add_group(request):
    choices = CATEGORY_CHOICES
    teachers = User.objects.filter(role=3)
    context = {
        'choices': choices,
        'teachers': teachers,
    }
    if request.POST:
        form = AddGroupForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            number = form.cleaned_data['number']
            category = request.POST['category']
            teacher = form.cleaned_data['teacher']
            form.year = year
            form.number = number
            form.category = category
            form.teacher = teacher
            form.start = request.POST['start']
            form.stop = request.POST['stop']
            form.save()
            messages.success(request, "Guruh qo'shildi")
    else:
        form = AddGroupForm()
    return render(request, 'user/add_group.html', context)


def groups_list(request):
    groups = Group.objects.all()
    context = {
        'groups': groups,
    }
    return render(request, 'user/groups_list.html', context)


def group_detail(request, id):
    group = Group.objects.get(id=id)
    pupils = User.objects.filter(role=4, group=group)
    context = {
        'group': group,
        'pupils': pupils,
    }
    return render(request, 'user/group_detail.html', context)