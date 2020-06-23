from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
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
        print(author)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = author
            form.save()
            messages.success(request, "Muvaffaqiyatli qo'shildi !")
            form = AddScheduleFrom()
        else:
            form = AddScheduleFrom(request.POST)
            messages.error(request, "Formani to'ldirishda xatolik !")
    else:
        form = AddScheduleFrom(request.POST)

    return render(request, 'sign/add_schedule.html', {
        'form': form
    })


@login_required
def add_subject(request):
    form = AddSubjectFrom()
    print(request.POST)
    if request.POST:
        form = AddSubjectFrom(request.POST)
        if form.is_valid():
            form.save()
            form = AddSubjectFrom()
            messages.success(request, "Muvaffaqiyatli qo'shildi !")
        else:
            form = AddSubjectFrom(request.POST)
            messages.error(request, "Formani to'ldirishda xatolik !")
    else:
        form = AddSubjectFrom(request.POST)
    return render(request, 'sign/add_subject.html', {
        'form': form
    })


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
            td += f"<tr>" \
                  f"<td>M-{schedule.sort}</td>" \
                  f"<td>{schedule.title}</td>" \
                  f"</tr>"
        return HttpResponse(td)
    else:
        return False
