from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from sign.forms import *
from sign.models import *


@login_required
def sign(request):
    signs = Sign.objects.all()
    return render(request, 'sign/signs.html', {
        'signs': signs,
    })


@login_required
def add_schedule(request):
    form = AddScheduleFrom()
    if request.POST:
        form = AddScheduleFrom(request.POST)
        author = User.objects.get(id=request.user.id)
        if form.is_valid():
            print(form.cleaned_data['title'])
            form = form.save(commit=False)
            form.author = author
            form.save()
            messages.success(request, "Muvaffaqiyatli qo'shildi !")
            form = AddScheduleFrom()
        else:
            messages.error(request, "Formani to'ldirishda xatolik !")
            form = AddScheduleFrom()
    else:
        form = AddScheduleFrom()

    return render(request, 'sign/add_schedule.html', {
        'form': form
    })


@login_required
def update_schedule(request, id):
    schedule = Schedule.objects.get(id=id)
    form = UpdateScheduleForm(instance=schedule)
    if request.POST:
        form = UpdateScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, "Muvaffaqiyatli tahrirlandi !")
        else:
            form = UpdateScheduleForm(instance=schedule)
            messages.error(request, "Formani to'ldirishda xatolik !")
    else:
        form = UpdateScheduleForm(instance=schedule)
    return render(request, 'sign/update_schedule.html', {
        'form': form,
        'schedule':schedule
    })


@login_required
def delete_schedule(request, id):
    schedule = Schedule.objects.get(id=id)
    schedule.delete()
    return render(request, 'sign/schedules_list.html',)

@login_required
def schedules_list(request):
    return render(request, 'sign/schedules_list.html')


def get_subject(request):
    if request.is_ajax():
        subjects = Subject.objects.filter(category=request.GET.get('category'))
        options = "<option>-- -- --</option>"
        for subject in subjects:
            options += f"<option value='{subject.id}'>{subject.title}</option>"
        return HttpResponse(options)
    else:
        return False


def get_schedule(request):
    if request.is_ajax():
        schedules = Schedule.objects.filter(subject=request.GET.get('subject'))
        td = ""

        for schedule in schedules:
            url_update = reverse_lazy('sign:update_schedule', kwargs={'id': schedule.id})
            url_delete = reverse_lazy('sign:delete_schedule', kwargs={'id': schedule.id})
            td += f"<tr>" \
                  f"<td>M-{schedule.sort}</td>" \
                  f"<td>{schedule.title}</td>" \
                  f"<td><a href='{url_update}'><i class='fa fa-edit'></i></a><a href='{url_delete}'><i class='fa fa-trash ml-2'></i></a></td>" \
                  f"</tr>"
        return HttpResponse(td)
    else:
        return False
