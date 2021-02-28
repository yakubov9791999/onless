from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse_lazy, reverse

from user.models import School, Region
from video.forms import SignUpSchoolForm


def landing_page(request):
    return render(request, 'corporate/index.html')


@login_required
def home(request):
    if request.user.role == "4" and request.user.school.is_block == False:  # agarda role o'quvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy("user:result", kwargs={'id': request.user.id}))


    elif request.user.role == "1":  # agarda role inspeksiya bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            schools = School.objects.filter(Q(region=request.user.school.region)& Q(is_active=True)).exclude(id=request.user.school.id)
            return render(request, 'user/inspection/schools_list.html', {
                'schools': schools,
            })

    elif request.user.role == "3" and request.user.school.is_block == False:  # agarda role o'qituvchi  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy("user:result", kwargs={'id': request.user.id}))


    elif request.user.role == "2" and request.user.school.is_block == False:  # agarda role Direktor  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy("user:result", kwargs={'id': request.user.id}))

    elif request.user.role == "5" and request.user.school.is_block == False:  # agarda role Bugalter  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy('user:bugalter_groups_list'))

    elif request.user.role == "6" and request.user.school.is_block == False:  # agarda role Instructor  bo'lsa
        if request.user.avatar == '' and request.user.birthday == '' and request.user.gender == '':
            return redirect(reverse_lazy('user:edit_profil'))
        else:
            return redirect(reverse_lazy("user:result", kwargs={'id': request.user.id}))
    else:
        return render(request, 'inc/block.html')


def sign_up(request):
    regions = Region.objects.all()
    context = {
        'regions': regions
    }

    if request.POST:
        form = SignUpSchoolForm(request.POST)
        viloyat = Region.objects.get(id=request.POST.get('viloyat'))
        if form.is_valid():
            if request.POST['select'] == '1':
                form = form.save(commit=False)
                form.viloyat = viloyat
                form.select = True
                form.save()
            elif request.POST['select'] == '0':
                form = form.save(commit=False)
                form.viloyat = viloyat
                form.select = False
                form.save()
            messages.success(request, 'Muvaffaqiyatli yuborildi !')
    return render(request, 'sign_up/index.html', context)

def kirish(request):
    return HttpResponseRedirect(reverse('account_login'))  # or http response
