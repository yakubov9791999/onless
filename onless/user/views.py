import random
import shutil
from random import randrange
from datetime import datetime as dt
import datetime
import requests
import xlrd
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import ProtectedError, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.views.generic import UpdateView
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter

from onless import settings
from onless.settings import BASE_DIR
from quiz.models import *
from sign.models import Material
from user.decorators import *

from .forms import *
from user.models import User, Group, CATEGORY_CHOICES, School
from video.views import *
from video.models import *
from .models import *
from django.db import IntegrityError

#
from .utils import render_to_pdf


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        username = get_pasport(username)
        password = request.POST['password'].replace(' ', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active and user.school.is_block == False:
                login(request, user)
                return redirect(reverse_lazy('video:home'))
            else:
                messages.error(request, 'Siz bloklangansiz !')
                return HttpResponseRedirect('/accounts/login/')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")
            return HttpResponseRedirect('/accounts/login/')


@login_required
def add_list(request):
    if request.user.role == '2' or request.user.role == '3':
        return render(request, 'inc/add_list.html')
    else:
        return render(request, 'inc/404.html')


@login_required
def settings_list(request):
    return render(request, 'user/settings_list.html')


@login_required
def add_teacher(request):
    if request.user.role == '2':
        if request.method == 'POST':
            form = AddUserForm(data=request.POST)
            password = random.randint(1000000, 9999999)
            if form.is_valid():
                name = form.cleaned_data['name']
                name = get_name(name)
                username = request.POST['pasport']
                username = get_pasport(username)
                try:
                    user = User.objects.create_user(
                        username=username,
                        pasport=username,
                        school=request.user.school,
                        turbo=password,
                        password=password,
                        name=name,
                        phone=form.cleaned_data['phone'],
                        role='3',
                        is_superuser=False,
                    )
                    user.set_password(password)
                    user.username = username
                    user.email = ''
                    user.save()

                    messages.success(request, "O'qituvchi muvaffaqiyatli qo'shildi")
                except IntegrityError:
                    messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
            else:
                messages.error(request, "Forma to'liq yoki to'g'ri to'ldirilmagan !")
        else:
            form = AddUserForm(request)
        return render(request, 'user/teacher/add_teacher.html', )
    else:
        return render(request, 'inc/404.html')


@login_required
def add_pupil(request):
    if request.user.role == '2' or request.user.role == '3':
        if request.user.role == '2':
            groups = Group.objects.filter(school=request.user.school, is_active=True).order_by('sort')
            if not groups.exists():
                messages.error(request, "O'quvchi qo'shish uchun avval guruh ro'yhatdan o'tkazing !")
        elif request.user.role == '3':
            teacher = User.objects.get(id=request.user.id)
            groups = Group.objects.filter(school=request.user.school, is_active=True, teacher=teacher).order_by('sort')
            if not groups.exists():
                messages.error(request, "O'quvchi qo'shish uchun avval guruh ro'yhatdan o'tkazing !")
        form = AddPupilForm()
        context = {
            'groups': groups,
            'form': form,
        }
        if request.method == 'POST':
            form = AddPupilForm(data=request.POST)
            group = get_object_or_404(Group, id=request.POST['group'])
            parol = random.randint(1000000, 9999999)
            pasport = request.POST['pasport']
            pasport = get_pasport(pasport)
            if form.is_valid():
                name = form.cleaned_data['name']
                name = get_name(name)
                try:
                    user = User.objects.create_user(
                        username=pasport,
                        pasport=pasport,
                        school=request.user.school,
                        turbo=parol,
                        password=parol,
                        name=name,
                        phone=form.cleaned_data['phone'],
                        role='4',
                        group=group,
                        is_superuser=False,
                    )
                    user.set_password(parol)
                    user.username = pasport
                    if request.POST['birthday']:
                        user.birthday = request.POST['birthday']
                    user.email = ''
                    user.save()
                    msg = f"Hurmatli {user.name}! Siz {user.group.category}-{user.group.number} guruhiga onlayn o'qish rejimida qabul qilindingiz. Darslarga qatnashish uchun http://onless.uz/kirish manziliga kiring. %0aLogin: {user.username}%0aParol: {user.turbo}%0aQo'shimcha savollar bo'lsa {user.school.phone} raqamiga qo'ng'iroq qilishingiz mumkin"
                    msg = msg.replace(" ", "+")
                    url = f"https://developer.apix.uz/index.php?app=ws&u={request.user.school.sms_login}&h={request.user.school.sms_token}&op=pv&to=998{user.phone}&msg={msg}"
                    response = requests.get(url)
                    messages.success(request, "O'quvchi muvaffaqiyatli qo'shildi")
                except IntegrityError:
                    messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
            else:
                messages.error(request, "Forma to'liq yoki to'g'ri to'ldirilmagan !")
        else:
            form = AddPupilForm()
        return render(request, 'user/pupil/add_pupil.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def add_group(request):
    if request.user.role == '2':
        teachers = User.objects.filter(
            Q(role=3, school=request.user.school) | Q(role=2, school=request.user.school)).order_by('name')
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
                if request.POST['price']:
                    price = request.POST['price']
                    form.price = price
                form.category = category
                form.teacher = teacher
                form.school = request.user.school
                form.start = request.POST['start']
                form.stop = request.POST['stop']
                form.save()
                messages.success(request, f"{form.category}-{form.number}-{form.year} guruh qo'shildi")
        else:
            form = AddGroupForm()
        return render(request, 'user/group/add_group.html', context)
    elif request.user.role == '3':
        if request.POST:
            form = AddTeacherGroupForm(request.POST)
            if form.is_valid():
                number = form.cleaned_data['number']
                category = request.POST['category']
                teacher = get_object_or_404(User, id=request.user.id)
                price = form.cleaned_data['price']
                form = form.save(commit=False)
                form.number = number
                form.price = price
                form.category = category
                form.teacher = teacher
                form.school = request.user.school
                form.start = request.POST['start']
                form.stop = request.POST['stop']
                form.save()
                messages.success(request, f"{form.category}-{form.number}-{form.year} guruh qo'shildi")
        else:
            form = AddTeacherGroupForm()
        return render(request, 'user/teacher/add_group.html')
    else:
        return render(request, 'inc/404.html')


@login_required
def groups_list(request):
    if request.user.role == '2':
        groups = Group.objects.filter(school=request.user.school, is_active=True).order_by('sort')
        if not groups.exists():
            messages.error(request, "Guruhlar mavjud emas avval guruh ro'yhatdan o'tkazing !")
        context = {
            'groups': groups,
        }
        return render(request, 'user/group/groups_list.html', context)
    elif request.user.role == '3':
        teacher = User.objects.get(id=request.user.id)
        groups = Group.objects.filter(school=request.user.school, teacher=teacher, is_active=True).order_by('sort')
        if not groups.exists():
            messages.error(request, "Guruhlar mavjud emas avval guruh ro'yhatdan o'tkazing !")
        context = {
            'groups': groups,
        }
        return render(request, 'user/group/groups_list.html', context)
    elif request.user.role == '4':
        pupil = get_object_or_404(User, id=request.user.id)
        groups = Group.objects.filter(id=pupil.group.id, school=request.user.school, is_active=True).order_by('sort')
        if not groups.exists():
            messages.error(request, "Guruhlar mavjud emas avval guruh ro'yhatdan o'tkazing !")

        context = {
            'groups': groups,
        }
        return render(request, 'user/group/groups_list.html', context)


    else:
        return render(request, 'inc/404.html')


@login_required
def group_detail(request, id):
    if request.user.role == '2' or request.user.role == '3' or request.user.role == '5':
        group = get_object_or_404(Group, id=id)
        pupils_list = User.objects.filter(role=4, school=request.user.school, group=group, is_active=True).order_by(
            'name')
        # pupils = []
        # for pupil in pupils_list:
        #     get_name(pupil.name.encode('UTF-8'))
        #     pupils.append(pupil)
        context = {
            'group': group,
            'pupils': pupils_list,
        }

        download = request.GET.get('download')
        if download:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response[
                'Content-Disposition'] = f'attachment; filename="{group.category}-{group.number} {group.year}.xlsx"'

            # create workbook
            wb = Workbook()

            sheet = wb.active
            sheet.alignment = Alignment(horizontal="center", vertical="center")
            # stylize header row
            # 'id','title', 'quantity','pub_date'
            trips_ws = wb.get_sheet_by_name("Sheet")
            trips_ws.column_dimensions['A'].width = 3
            trips_ws.column_dimensions['B'].width = 40
            trips_ws.column_dimensions['C'].width = 15
            trips_ws.column_dimensions['D'].width = 15
            trips_ws.column_dimensions['E'].width = 15

            c1 = sheet.cell(row=1, column=1)

            c1.value = "#"
            c1.font = Font(bold=True)

            c2 = sheet.cell(row=1, column=2)
            c2.value = "F.I.O"
            c2.font = Font(bold=True)

            c3 = sheet.cell(row=1, column=3)
            c3.value = "Tel raqam"
            c3.font = Font(bold=True)

            c4 = sheet.cell(row=1, column=4)
            c4.value = "Login"
            c4.font = Font(bold=True)

            c5 = sheet.cell(row=1, column=5)
            c5.value = "Parol"
            c5.font = Font(bold=True)

            # export data to Excel
            rows = pupils_list.values_list('name', 'phone', 'username', 'turbo')

            for row_num, row in enumerate(rows, 1):
                i = 1
                # row is just a tuple
                for col_num, value in enumerate(row):
                    r2 = sheet.cell(row=row_num + 1, column=col_num + 2)
                    r2.value = value
                    # forloop = sheet.cell(column=1, row=row_num + 1)
                    # forloop.value = '#'

                i = + 1
            wb.save(response)

            return response
        return render(request, 'user/group/group_detail.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def group_delete(request, id):
    if request.user.role == '2':
        group = get_object_or_404(Group, id=id)
        if group.group_user.count() > 2:
            group.is_active = False
            group.save()
        else:
            group.delete()
    else:
        return render(request, 'inc/404.html')


@login_required
def group_update(request, id):
    if request.user.role == '2' or request.user.role == '3':
        group = get_object_or_404(Group, id=id)
        form = GroupUpdateForm(instance=group, user=request.user)
        if request.POST:
            form = GroupUpdateForm(request.POST, instance=group, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Guruh muvaffaqiyatli tahrirlandi !")
            else:
                messages.error(request, "Formani to'ldirishda xatolik !")
        else:
            form = GroupUpdateForm(instance=group, user=request.user)
        context = {
            'form': form,
            'group': group,
        }
        return render(request, 'user/group/group_update.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def profil_edit(request):
    user = get_object_or_404(User, id=request.user.id)
    form = EditUserForm(instance=user)
    if request.POST:
        form = EditUserForm(request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            name = form.cleaned_data['name']
            name = get_name(name)
            form = form.save(commit=False)
            form.name = name
            password = user.set_password(request.POST['turbo'])
            form.save()
            user = authenticate(username=request.user.username, password=request.POST['turbo'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    form = EditUserForm(instance=user)
            messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
        else:
            messages.error(request, "Formani to'ldirishda xatolik !")
    else:
        form = EditUserForm(instance=user)
    context = {
        'form': form
    }
    return render(request, 'user/profil_edit.html', context)


@login_required
def school_edit(request):
    if request.user.role == '2':
        school = get_object_or_404(School, id=request.user.school.id)
        form = EditSchoolForm(instance=request.user.school)
        if request.POST:
            form = EditSchoolForm(request.POST or None, request.FILES or None, instance=request.user.school)
            if form.is_valid():
                form.save()
                messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
            else:
                messages.error(request, "Formani to'ldirishda xatolik !")
        else:
            form = EditSchoolForm(instance=request.user.school)
        context = {
            'form': form
        }
        return render(request, 'user/school/school_edit.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def pupil_edit(request, id):
    if request.user.role == '2' or request.user.role == '3':
        user = get_object_or_404(User, id=id)
        form = EditPupilForm(instance=user, request=request)
        if request.POST:
            pasport = request.POST['pasport']
            print(pasport)
            pasport = get_pasport(pasport)
            form = EditPupilForm(request.POST, request.FILES, instance=user, request=request)
            if form.is_valid():
                name = form.cleaned_data['name']
                name = get_name(name)
                form = form.save(commit=False)
                form.name = name
                form.pasport = pasport
                form.username = pasport
                user.set_password(request.POST['turbo'])
                form.save()
                messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
                form = EditPupilForm(instance=user, request=request)
            else:
                messages.error(request, "Formani to'ldirishda xatolik !")
        else:
            form = EditPupilForm(instance=user, request=request)
        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'user/pupil/pupil_edit.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def contact(request):
    if request.POST or None:
        form = AddContactForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            text = form.cleaned_data['text']
            photo = request.POST['photo']
            form = form.save(commit=False)
            form.text = text
            form.user = request.user
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
    try:
        query = request.GET.get('q', False).lower()

        context = {
            'q': query,
        }

        count = 0

        if query:
            try:
                teachers = User.objects.filter(Q(pasport__icontains=query) |
                                               Q(name__icontains=query)).filter(role=3, school=request.user.school,
                                                                                is_active=True).order_by('name')
                context.update(teachers=teachers)

                count += teachers.count()
            except ValueError:
                pass

            try:
                bugalters = User.objects.filter(Q(pasport__icontains=query) |
                                                Q(name__icontains=query)).filter(role=5, school=request.user.school,
                                                                                 is_active=True).order_by('name')
                context.update(bugalters=bugalters)

                count += bugalters.count()
            except ValueError:
                pass

            try:
                pupils = User.objects.filter(Q(pasport__icontains=query) |
                                             Q(name__icontains=query)).filter(role=4,
                                                                              school=request.user.school,
                                                                              is_active=True).order_by('name')

                context.update(pupils=pupils)

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

                count += groups.count()
            except ValueError:
                pass

            try:
                videos = Video.objects.filter(
                    title__icontains=query, is_active=True
                ).distinct()

                context.update(videos=videos)
                count += videos.count()
            except ValueError:
                pass

            try:
                materials = Material.objects.filter(
                    title__icontains=query, is_active=True
                ).distinct()

                context.update(materials=materials)
                count += materials.count()
            except ValueError:
                pass
            context.update(count=count)

        return render(request, 'user/search_result.html', context)
    except AttributeError:
        return redirect(reverse_lazy('video:home'))

@login_required
def pupil_delete(request, id):
    if request.user.role == '2':
        pupil = get_object_or_404(User, id=id)
        pupil.is_active = False
        pupil.save()
    else:
        return render(request, 'inc/404.html')


@login_required
def workers_list(request):
    if request.user.role == '2':
        workers = User.objects.filter(
            Q(school=request.user.school, role=5, is_active=True) | Q(school=request.user.school, role=3,
                                                                      is_active=True)).order_by('name')
        if not workers.exists():
            messages.error(request, "Xodimlar ro'yhatga olinmagan !")
        context = {
            'workers': workers
        }
        return render(request, 'user/workers_list.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def worker_edit(request, id):
    if request.user.role == '2':
        worker = get_object_or_404(User, id=id)
        form = EditWorkerForm(instance=worker)
        if request.POST:
            pasport = get_pasport(request.POST['pasport'])
            form = EditWorkerForm(request.POST, request.FILES, instance=worker)
            if form.is_valid():
                form = form.save(commit=False)
                form.pasport = pasport
                form.username = pasport
                worker.set_password(request.POST['turbo'])
                form.save()
                messages.success(request, 'Muvaffaqiyatli tahrirlandi !')
                form = EditWorkerForm(instance=worker)
            else:
                messages.error(request, "Formani to'ldirishda xatolik !")
        else:
            form = EditWorkerForm(instance=worker)
        context = {
            'worker': worker,
            'form': form
        }
        return render(request, 'user/worker_edit.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def worker_delete(request, id):
    if request.user.role == '2':
        worker = get_object_or_404(User, id=id)
        worker.is_active = False
        worker.save()
    else:
        return render(request, 'inc/404.html')


@login_required
def upload_file(request):
    if request.user.role == '2' or request.user.role == '3':
        if request.POST and request.FILES:
            file = request.FILES['file']
            file = File.objects.create(file=file)
            if settings.DEBUG:
                file_path = os.path.join(f'{BASE_DIR}{os.path.sep}media{os.path.sep}{file.file}')
            else:
                file_path = os.path.join(
                    f'{os.path.sep}home{os.path.sep}users{os.path.sep}b{os.path.sep}bcloudintelekt{os.path.sep}domains{os.path.sep}onless.uz{os.path.sep}media{os.path.sep}{file.file}')
            group = get_object_or_404(Group, id=request.POST['group'])
            wb = xlrd.open_workbook(file_path)
            sheet = wb.sheet_by_index(0)
            number_of_rows = sheet.nrows
            number_of_columns = sheet.ncols

            for row in range(1, number_of_rows):
                i = 2
                i = i + 1
                name = str((sheet.cell(row, 1).value))
                name = get_name(name)

                pasport = (sheet.cell(row, 2).value)
                pasport = get_pasport(pasport)

                if len(str(pasport)) >= 7 and len(str(pasport)) < 9:
                    messages.error(request, f"Excel fayldagi {row + 1}-ustunda pasport noto'g'ri kiritilgan ! ")
                    break

                if not name:
                    messages.error(request, f"Excel fayldagi {row + 1}-ustunda ism kiritilmagan ! ")
                    break

                split_phone = str((sheet.cell(row, 3).value)).split('.')

                try:
                    phone = int(split_phone[0])

                    try:
                        try:
                            parol = random.randint(1000000, 9999999)
                            user = User.objects.create_user(
                                username=pasport,
                                pasport=pasport,
                                school=request.user.school,
                                turbo=parol,
                                password=parol,
                                name=name,
                                phone=int(phone),
                                role='4',
                                group=group,
                                is_superuser=False,
                            )
                            user.set_password(parol)
                            user.username = pasport
                            user.email = ''
                            user.save()
                            msg = f"Hurmatli {user.name}! Siz {user.group.category}-{user.group.number} guruhiga onlayn o'qish rejimida qabul qilindingiz. Darslarga qatnashish uchun http://onless.uz/kirish manziliga kiring. %0aLogin: {user.username}%0aParol: {user.turbo}%0aQo'shimcha savollar bo'lsa {user.school.phone} raqamiga qo'ng'iroq qilishingiz mumkin"
                            msg = msg.replace(" ", "+")
                            url = f"https://developer.apix.uz/index.php?app=ws&u={request.user.school.sms_login}&h={request.user.school.sms_token}&op=pv&to=998{user.phone}&unicode=1&msg={msg}"
                            response = requests.get(url)
                            messages.success(request, f"Muvaffaqiyatli qo'shildi !")


                        except IntegrityError:
                            messages.error(request, f"{pasport} pasport oldin ro'yhatdan o'tkazilgan !")
                            next = request.META['HTTP_REFERER']
                            return HttpResponseRedirect(next)


                    except UnboundLocalError:
                        messages.error(request, "Formani to'liq to'ldiring !")
                        next = request.META['HTTP_REFERER']
                        return HttpResponseRedirect(next)


                except ValueError:
                    phone = None

                    try:
                        try:
                            parol = random.randint(1000000, 9999999)
                            user = User.objects.create_user(
                                username=pasport,
                                pasport=pasport,
                                school=request.user.school,
                                turbo=parol,
                                password=parol,
                                name=name,
                                phone=phone,
                                role='4',
                                group=group,
                                is_superuser=False,
                            )
                            user.set_password(parol)
                            user.username = pasport
                            user.email = ''
                            user.save()
                            messages.success(request, f"Muvaffaqiyatli qo'shildi !")
                            # messages.error(request, f"Excel fayldagi {row + 1}-ustunda xatolik ! ")
                            # next = request.META['HTTP_REFERER']
                            # return HttpResponseRedirect(next)

                        except IntegrityError:
                            messages.error(request, f"{pasport} pasport oldin ro'yhatdan o'tkazilgan !")
                            next = request.META['HTTP_REFERER']
                            return HttpResponseRedirect(next)

                    except UnboundLocalError:
                        messages.error(request, "Formani to'liq to'ldiring !")
                        next = request.META['HTTP_REFERER']
                        return HttpResponseRedirect(next)

            next = request.META['HTTP_REFERER']
            return HttpResponseRedirect(next)
        else:
            messages.error(request, "Faylni kiriting !")
            next = request.META['HTTP_REFERER']
            return HttpResponseRedirect(next)
    else:
        return render(request, 'inc/404.html')


@login_required
def add_bugalter(request):
    if request.user.role == '2':
        if request.POST:
            form = AddUserForm(data=request.POST)
            password = random.randint(1000000, 9999999)
            pasport = get_pasport(request.POST['pasport'])
            if form.is_valid():
                name = form.cleaned_data['name']
                name = get_name(name)
                try:
                    user = User.objects.create_user(
                        username=pasport,
                        pasport=pasport,
                        school=request.user.school,
                        turbo=password,
                        password=password,
                        name=name,
                        phone=form.cleaned_data['phone'],
                        role='5',
                        is_superuser=False,
                    )
                    user.set_password(password)
                    user.username = pasport
                    user.email = ''
                    user.save()
                    messages.success(request, "Hisobchi muvaffaqiyatli qo'shildi")

                except IntegrityError:
                    messages.error(request, "Bu pasport oldin ro'yhatdan o'tkazilgan !")
            else:
                messages.error(request, "Formani to'liq yoki to'g'ri to'ldirilmagan !")
        else:
            form = AddUserForm(request)
        return render(request, 'user/bugalter/add_bugalter.html')
    else:
        return render(request, 'inc/404.html')


@login_required
def bugalter_groups_list(request):
    if request.user.role == '2' or request.user.role == '5':
        groups = Group.objects.filter(school=request.user.school, is_active=True).order_by('sort')
        if not groups.exists():
            messages.error(request, "Guruhlar mavjud emas avval guruh ro'yhatdan o'tkazing !")
        context = {
            'groups': groups
        }
        return render(request, 'user/bugalter/groups_list.html', context)
    elif request.user.role == '3':
        teacher = get_object_or_404(User, id=request.user.id)
        groups = Group.objects.filter(school=request.user.school, teacher=teacher, is_active=True).order_by('sort')
        if not groups.exists():
            messages.error(request, "Guruhlar mavjud emas avval guruh ro'yhatdan o'tkazing !")
        context = {
            'groups': groups
        }
        return render(request, 'user/bugalter/groups_list.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def bugalter_group_detail(request, id):
    if request.user.role == '2' or request.user.role == '5' or request.user.role == '3':
        group = get_object_or_404(Group, id=id)
        pupils = User.objects.filter(role=4, school=request.user.school, group=group, is_active=True).order_by('name')
        total_pay = group.price * pupils.count()
        payments = Pay.objects.filter(pupil__in=pupils)
        if not payments.exists():
            messages.error(request, "To'lovlar mavjud emas !")
        total_payments = 0
        for pay in payments:
            total_payments += pay.payment
        total_debit = total_pay - total_payments
        context = {
            'group': group,
            'pupils': pupils,
            'total_pay': total_pay,
            'total_payments': total_payments,
            'total_debit': total_debit
        }
        return render(request, 'user/bugalter/group_detail.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def add_pay(request):
    if request.user.role == '5':
        if request.POST:
            if not request.POST['pay'] == '0':
                pupil = get_object_or_404(User, id=request.POST['pupil'])
                group = get_object_or_404(Group, id=request.POST['group'])
                values = Pay.objects.filter(pupil=pupil)
                payment = 0
                for value in values:
                    payment += value.payment
                payment += int(request.POST['pay'])
                if group.price >= payment:
                    Pay.objects.create(pupil=pupil, payment=int(request.POST['pay']))
                    messages.success(request, "O'qish puli muvaffaqiyatli qo'shildi !")
                else:
                    messages.error(request, f"O'qish puli {group.price} dan ortiq bo'lishi mumkin emas !")
            else:
                messages.error(request, "Summani to'g'ri kiriting !")
        next = request.META['HTTP_REFERER']
        return HttpResponseRedirect(next)
    else:
        return render(request, 'inc/404.html')


@login_required
def pay_history(request, user_id, group_id):
    if request.user.role == '5' or request.user.role == '2' or request.user.role == '4' or request.user.role == '3':
        pupil = get_object_or_404(User, id=user_id)
        payments = Pay.objects.filter(pupil=pupil)
        if not payments.exists():
            messages.error(request, "To'lov amalga oshirilmagan !")
        group = get_object_or_404(Group, id=group_id)

        context = {
            'pupil': pupil,
            'payments': payments,
            'group': group
        }
        return render(request, 'user/bugalter/pay_history.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def history_view_video_all(request):
    if request.user.role == '2':
        groups = Group.objects.filter(school=request.user.school)
        context = {
            'groups': groups,
        }
        if request.POST:
            if request.POST['startdate']:
                startdate = request.POST['startdate']
                # strokadan time formatga o'tkazish
                # filtrlash uchun soat min secund qo'shish
                startdate = dt.strptime(startdate, '%Y-%m-%d')
                startdate = datetime.datetime.combine(startdate, datetime.time.min)
            else:
                startdate = '2020-06-01'

            context.update(startdate=request.POST['startdate'])

            if request.POST['stopdate']:
                stopdate = request.POST['stopdate']
                # 2020-07-03 23:59:59.999999
                # <class 'datetime.datetime'>
                stopdate = dt.strptime(stopdate, '%Y-%m-%d')
                stopdate = datetime.datetime.combine(stopdate, datetime.time.max)
            else:
                stopdate = datetime.date.today()
                stopdate = datetime.datetime.combine(stopdate, datetime.time.max)

            context.update(stopdate=request.POST['stopdate'])

            if request.POST['group'] != 'False':
                group = get_object_or_404(Group, id=request.POST['group'])
                pupils = User.objects.filter(group=group)
                views = ViewComplete.objects.filter(Q(user__school=request.user.school) & Q(user__in=pupils) & Q(
                    time__range=[startdate, stopdate])).order_by('-time')
                if not views.exists():
                    messages.error(request, "Ko'rishlar mavjud emas !")
                context.update(views=views, guruh=group)
            else:
                views = ViewComplete.objects.filter(Q(user__school=request.user.school) & Q(user__role=4) & Q(
                    time__range=[startdate, stopdate])).order_by('-time')
                if not views.exists():
                    messages.error(request, "Ko'rishlar mavjud emas !")
                context.update(views=views)
                print('ok')
            return render(request, 'user/view_video_history_all.html', context)
        else:
            views = ViewComplete.objects.filter(
                Q(user__school=request.user.school, ) & Q(user__role=4) & Q(user__is_active=True)).order_by(
                '-time')
            if not views.exists():
                messages.error(request, "Ko'rishlar mavjud emas !")
            context.update(views=views)
            return render(request, 'user/view_video_history_all.html', context)

    elif request.user.role == '3':
        teacher = get_object_or_404(User, id=request.user.id)
        groups = Group.objects.filter(teacher=teacher).order_by('sort')
        pupils = User.objects.filter(group__in=groups)
        context = {
            'groups': groups
        }
        if request.POST:
            if request.POST['startdate']:
                startdate = request.POST['startdate']
                # strokadan time formatga o'tkazish
                # filtrlash uchun soat min secund qo'shish
                startdate = dt.strptime(startdate, '%Y-%m-%d')
                startdate = datetime.datetime.combine(startdate, datetime.time.min)
            else:
                startdate = '2020-06-01'

            context.update(startdate=request.POST['startdate'])

            if request.POST['stopdate']:
                stopdate = request.POST['stopdate']
                # 2020-07-03 23:59:59.999999
                # <class 'datetime.datetime'>
                stopdate = dt.strptime(stopdate, '%Y-%m-%d')
                stopdate = datetime.datetime.combine(stopdate, datetime.time.max)
            else:
                stopdate = datetime.date.today()
                stopdate = datetime.datetime.combine(stopdate, datetime.time.max)

            context.update(stopdate=request.POST['stopdate'])

            if request.POST['group'] != 'False':
                group = get_object_or_404(Group, id=request.POST['group'])
                pupils = User.objects.filter(group=group)
                views = ViewComplete.objects.filter(Q(user__school=request.user.school) & Q(user__in=pupils) & Q(
                    time__range=[startdate, stopdate])).order_by('-time')
                if not views.exists():
                    messages.error(request, "Ko'rishlar mavjud emas !")
                context.update(views=views)
                return render(request, 'user/view_video_history_all.html', context)
            views = ViewComplete.objects.filter(Q(user__school=request.user.school) & Q(user__in=pupils) & Q(
                time__range=[startdate, stopdate])).order_by('-time')
            if not views.exists():
                messages.error(request, "Ko'rishlar mavjud emas !")
            context.update(views=views)
            return render(request, 'user/view_video_history_all.html', context)
        else:
            views = ViewComplete.objects.filter(Q(user__school=request.user.school) & Q(user__in=pupils)).order_by(
                '-time')
            if not views.exists():
                messages.error(request, "Ko'rishlar mavjud emas !")
            context.update(views=views)
            return render(request, 'user/view_video_history_all.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def history_pupil_view_video(request, id):
    if request.user.role == '2' or request.user.role == '3' or request.user.role == '4':
        pupil = get_object_or_404(User, id=id)
        videos = Video.objects.filter(is_active=True).order_by('id')
        if not videos.exists():
            messages.error(request, "Ko'rishlar mavjud emas !")
        context = {
            'videos': videos,
            'pupil': pupil
        }
        return render(request, 'user/pupil/history_pupil_view_video.html', context)
    else:
        return render(request, 'inc/404.html')


@login_required
def get_district(request):
    if request.is_ajax():
        districts = District.objects.filter(region=request.GET.get('region'))
        options = "<option>--- --- ---</option>"
        for district in districts:
            options += f"<option value='{district.id}'>{district.title}</option>"
        return HttpResponse(options)
    else:
        return False


@login_required
def school_groups(request, id):
    school = get_object_or_404(School, id=id)
    groups = Group.objects.filter(school=school, is_active=True).order_by('sort')
    context = {
        'groups': groups
    }
    return render(request, 'user/inspection/school_groups.html', context)


@login_required
def school_group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    pupils = User.objects.filter(group=group, is_active=True).order_by('name')
    context = {
        'pupils': pupils,
        'group': group
    }
    return render(request, 'user/inspection/school_group_detail.html', context)


@login_required
def support(request):
    return render(request, 'user/messeges.html')


@login_required
def pupil_result(request, id):
    pupil = get_object_or_404(User, id=id)
    if request.user == pupil:
        return render(request, 'user/pupil/pupil_result.html')
    else:
        return render(request, 'inc/404.html')


@login_required
def messeges(request):
    return render(request, 'user/messeges.html')
