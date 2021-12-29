from abc import ABC
from django.shortcuts import get_object_or_404
from django.db.models import Max, Sum
from django.db.models import FloatField
from allauth.account.utils import user_username
from django.contrib import messages
from django.db.models import Sum
from django.db.models.signals import pre_save
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import csrf
from django.utils.safestring import SafeString
from django.views import View
from numpy import quantile
from pandas._libs.tslibs.base import ABCTimestamp
from suds.xsd import qualify

from quiz.models import *
from practical.models import *
from user.models import *
from video.models import *
from sign.models import *
from clinet.forms import *


def login_required_decorator(f):
    return login_required(f, login_url="login")


@login_required_decorator
def dashboard(request):
    user = User.objects.all().count()
    school = School.objects.all().count()
    group = Group.objects.all().count()
    pay = Pay.objects.all().aggregate(Sum('payment'))
    a = Pay.objects.all()
    b = 0
    for i in a:
        b = b + i.payment
    ctx = {
        'user': user,
        'pay': pay,
        'school': school,
        'group': group,
        'b': b
    }
    return render(request, 'dashboard/index.html', ctx)


def dashboard_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'dashboard/login.html')


@login_required_decorator
def dashboard_logout(request):
    logout(request)
    return redirect('login')


@login_required_decorator
def carmodel_list(request):

    carmodel = CarModel.objects.all()
    ctx = {
        'carmodel': carmodel,
        "c_active": 'active'
    }
    return render(request, 'dashboard/categories/list.html', ctx)


@login_required_decorator
def carmodel_create(request):
    model = CarModel()
    form = CarModelForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('carmodel_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/categories/form.html', ctx)


@login_required_decorator
def carmodel_edit(request, pk):
    model = CarModel.objects.get(id=pk)
    form = CarModelForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('carmodel_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/categories/form.html', ctx)


@login_required_decorator
def carmodel_delete(request, pk):
    model = CarModel.objects.get(id=pk)
    model.delete()
    return redirect('carmodel_list')


@login_required_decorator
def car_list(request):
    car = Car.objects.all()
    ctx = {
        'car': car,
        "c_active": 'active'
    }
    return render(request, 'dashboard/kontak/list.html', ctx)


@login_required_decorator
def car_create(request):
    model = Car()
    form = CarForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('car_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'instructors':User.objects.filter(role='6')
    }
    return render(request, 'dashboard/kontak/form.html', ctx)


@login_required_decorator
def car_edit(request, pk):
    model = Car.objects.get(id=pk)
    form = CarForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('car_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/kontak/form.html', ctx)


@login_required_decorator
def car_delete(request, pk):
    model = Car.objects.get(id=pk)
    model.delete()
    return redirect('car_list')


@login_required_decorator
def practical_list(request):
    practical = Practical.objects.all()
    ctx = {
        'practical': practical,
        "c_active": 'active'
    }
    return render(request, 'dashboard/products/list.html', ctx)


@login_required_decorator
def practical_create(request):
    model = Practical()
    form = PracticalForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('practical_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        "teachers": User.objects.filter(role='4'),
        'pupils':User.objects.filter(role='3')
    }
    return render(request, 'dashboard/products/form.html', ctx)


@login_required_decorator
def practical_edit(request, pk):
    model = Practical.objects.get(id=pk)
    form = PracticalForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('practical_list')
    ctx = {
        "form": form,
        'pupils': User.objects.filter(role='4'),
        'teachers': User.objects.filter(role='3'),
    }

    return render(request, 'dashboard/products/form.html', ctx)


@login_required_decorator
def practical_delete(request, pk):
    model = Practical.objects.get(id=pk)
    model.delete()
    return redirect('practical_list')


@login_required_decorator
def paymentforpractical_list(request):
    paymentforpractical = PaymentForPractical.objects.all()
    b=0
    for i in paymentforpractical:
        b +=i.sum
    ctx = {
        'paymentforpractical': paymentforpractical,
        "m_active": 'active',
        'b': b
    }
    return render(request, 'dashboard/paymentforpractical/list.html', ctx)


@login_required_decorator
def paymentforpractical_create(request):
    model = PaymentForPractical()
    form = PaymentForPracticalForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('paymentforpractical_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'pupils':User.objects.filter(role='4')
    }
    return render(request, 'dashboard/paymentforpractical/form.html', ctx)


@login_required_decorator
def paymentforpractical_edit(request, pk):
    model = PaymentForPractical.objects.get(id=pk)
    form = PaymentForPracticalForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('paymentforpractical_list')
    ctx = {
        "form": form,
        'pupils': User.objects.filter(role='4'),
        # 'teachers': User.objects.filter(role='3'),
    }
    return render(request, 'dashboard/paymentforpractical/form.html', ctx)


@login_required_decorator
def paymentforpractical_delete(request, pk):
    model = PaymentForPractical.objects.get(id=pk)
    model.delete()
    return redirect('paymentforpractical_list')


@login_required_decorator
def answer_list(request):
    answer = Answer.objects.all()
    ctx = {
        'answer': answer,
        "y_active": 'active'
    }
    return render(request, 'dashboard/answer/list.html', ctx)


@login_required_decorator
def answer_create(request):
    model = Answer()
    form = AnswerForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('answer_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/answer/form.html', ctx)


@login_required_decorator
def answer_edit(request, pk):
    model = Answer.objects.get(id=pk)
    form = AnswerForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('clinet.views.practical_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/answer/form.html', ctx)


@login_required_decorator
def answer_delete(request, pk):
    model = Answer.objects.get(id=pk)
    model.delete()
    return redirect('answer_list')


@login_required_decorator
def question_list(request):
    question = Question.objects.all()
    ctx = {
        'question': question,
        "v_active": 'active'
    }
    return render(request, 'dashboard/question/list.html', ctx)


@login_required_decorator
def question_create(request):
    model = Question()
    form = QuestionForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('question_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/question/form.html', ctx)


@login_required_decorator
def question_edit(request, pk):
    model = Question.objects.get(id=pk)
    form = QuestionForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('clinet.views.practical_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/question/form.html', ctx)


@login_required_decorator
def question_delete(request, pk):
    model = Question.objects.get(id=pk)
    model.delete()
    return redirect('question_list')


@login_required_decorator
def bilet_list(request):
    bilet = Bilet.objects.all()
    ctx = {
        'bilet': bilet,
        "l_active": 'active'
    }
    return render(request, 'dashboard/bilet/list.html', ctx)


@login_required_decorator
def bilet_create(request):
    model = Bilet()
    form = BiletForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('bilet_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/bilet/form.html', ctx)


@login_required_decorator
def bilet_edit(request, pk):
    model = Bilet.objects.get(id=pk)
    form = BiletForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('bilet_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/bilet/form.html', ctx)


@login_required_decorator
def bilet_delete(request, pk):
    model = Bilet.objects.get(id=pk)
    model.delete()
    return redirect('bilet_list')


@login_required_decorator
def savol_list(request):
    savol = Savol.objects.all()
    ctx = {
        'savol': savol,
        "x_active": 'active'
    }
    return render(request, 'dashboard/savol/list.html', ctx)


@login_required_decorator
def savol_create(request):
    model = Savol()
    form = SavolForm(request.POST, request.FILES, instance=model)
    print(form, 'SALOM')
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('savol_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/savol/form.html', ctx)


@login_required_decorator
def savol_edit(request, pk):
    model = Savol.objects.get(id=pk)
    form = SavolForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('savol_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/savol/form.html', ctx)


@login_required_decorator
def savol_delete(request, pk):
    model = Savol.objects.get(id=pk)
    model.delete()
    return redirect('savol_list')


@login_required_decorator
def javob_list(request):
    javob = Javob.objects.all()
    ctx = {
        'javob': javob,
        "z_active": 'active'
    }
    return render(request, 'dashboard/javob/list.html', ctx)


@login_required_decorator
def javob_create(request):
    model = Javob()
    form = JavobForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('javob_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/javob/form.html', ctx)


@login_required_decorator
def javob_edit(request, pk):
    model = Javob.objects.get(id=pk)
    form = JavobForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('javob_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/javob/form.html', ctx)


@login_required_decorator
def javob_delete(request, pk):
    model = Javob.objects.get(id=pk)
    model.delete()
    return redirect('javob_list')


@login_required_decorator
def result_list(request):
    result = Result.objects.all()
    ctx = {
        'result': result,
        "a_active": 'active'
    }
    return render(request, 'dashboard/result/list.html', ctx)


@login_required_decorator
def result_create(request):
    model = Result()
    form = ResultForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('result_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'pupils':User.objects.filter(role='4')
    }
    return render(request, 'dashboard/result/form.html', ctx)


@login_required_decorator
def result_edit(request, pk):
    model = Result.objects.get(id=pk)
    form = ResultForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('result_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/result/form.html', ctx)


@login_required_decorator
def result_delete(request, pk):
    model = Result.objects.get(id=pk)
    model.delete()
    return redirect('result_list')


@login_required_decorator
def resultquiz_list(request):
    resultquiz = Result.objects.all()
    ctx = {
        'resultquiz': resultquiz,
        "s_active": 'active'
    }
    return render(request, 'dashboard/resultquiz/list.html', ctx)


@login_required_decorator
def resultquiz_create(request):
    model = ResultQuiz()
    form = ResultQuizForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('resultquiz_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'pupils':User.objects.filter(role='4')
    }
    return render(request, 'dashboard/resultquiz/form.html', ctx)


@login_required_decorator
def resultquiz_edit(request, pk):
    model = ResultQuiz.objects.get(id=pk)
    form = ResultQuizForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('resultquiz_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/resultquiz/form.html', ctx)


@login_required_decorator
def resultquiz_delete(request, pk):
    model = ResultQuiz.objects.get(id=pk)
    model.delete()
    return redirect('resultquiz_list')


@login_required_decorator
def attempt_list(request):
    attempt = Attempt.objects.all()
    ctx = {
        'attempt': attempt,
        "f_active": 'active'
    }
    return render(request, 'dashboard/attempt/list.html', ctx)


@login_required_decorator
def attempt_create(request):
    model = Attempt()
    form = AttemptForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('attempt_list')
        else:
            print(form.errors, 'qwekfewjkfejkjkefwfkj')
    ctx = {
        "form": form,
        'pupils': User.objects.filter(role='4')
    }
    return render(request, 'dashboard/attempt/form.html', ctx)


@login_required_decorator
def attempt_edit(request, pk):
    model = Attempt.objects.get(id=pk)
    form = AttemptForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('attempt_list')
    ctx = {
        "form": form,
        'pupils': User.objects.filter(role='4')

    }
    return render(request, 'dashboard/attempt/form.html', ctx)


@login_required_decorator
def attempt_delete(request, pk):
    model = Attempt.objects.get(id=pk)
    model.delete()
    return redirect('attempt_list')


@login_required_decorator
def resultjavob_list(request):
    resultjavob = ResultJavob.objects.all()
    ctx = {
        'resultjavob': resultjavob,
        "g_active": 'active'
    }
    return render(request, 'dashboard/resultjavob/list.html', ctx)


@login_required_decorator
def resultjavob_create(request):
    model = ResultJavob()
    form = ResultForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('resultjavob_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'user':User.objects.filter(role='4'),
        'bilet':Bilet.objects.all()
    }
    return render(request, 'dashboard/resultjavob/form.html', ctx)


@login_required_decorator
def resultjavob_edit(request, pk):
    model = ResultJavob.objects.get(id=pk)
    form = ResultJavobForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('resultjavob_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/resultjavob/form.html', ctx)


@login_required_decorator
def resultjavob_delete(request, pk):
    model = ResultJavob.objects.get(id=pk)
    model.delete()
    return redirect('resultjavob_list')


@login_required_decorator
def checktestcolor_list(request):
    checktestcolor = CheckTestColor.objects.all()
    ctx = {
        'checktestcolor': checktestcolor,
        "h_active": 'active'
    }
    return render(request, 'dashboard/checktestcolor/list.html', ctx)


@login_required_decorator
def checktestcolor_create(request):
    model = CheckTestColor()
    form = CheckTestColorForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('checktestcolor_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'users':User.objects.filter(role='3')
    }
    return render(request, 'dashboard/checktestcolor/form.html', ctx)


@login_required_decorator
def checktestcolor_edit(request, pk):
    model = CheckTestColor.objects.get(id=pk)
    form = CheckTestColorForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('checktestcolor_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/checktestcolor/form.html', ctx)


@login_required_decorator
def checktestcolor_delete(request, pk):
    model = CheckTestColor.objects.get(id=pk)
    model.delete()
    return redirect('checktestcolor_list')


@login_required_decorator
def signcategory_list(request):
    signcategory = SignCategory.objects.all()
    ctx = {
        'signcategory': signcategory,
        "j_active": 'active'
    }
    return render(request, 'dashboard/singcategory/list.html', ctx)


@login_required_decorator
def signcategory_create(request):
    model = SignCategory()
    form = SignCategoryForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('signcategory_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/singcategory/form.html', ctx)


@login_required_decorator
def signcategory_edit(request, pk):
    model = SignCategory.objects.get(id=pk)
    form = SignCategoryForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('signcategory_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/singcategory/form.html', ctx)


@login_required_decorator
def signcategory_delete(request, pk):
    model = SignCategory.objects.get(id=pk)
    model.delete()
    return redirect('signcategory_list')


@login_required_decorator
def sign_list(request):
    sign = ResultJavob.objects.all()
    ctx = {
        'sign': sign,
        "k_active": 'active'
    }
    return render(request, 'dashboard/sign/list.html', ctx)


@login_required_decorator
def sign_create(request):
    model = Sign()
    form = SignForm(request.POST, request.FILES, instance=model)
    print(form, 'SASA')
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('sign_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/sign/form.html', ctx)


@login_required_decorator
def sign_edit(request, pk):
    model = Sign.objects.get(id=pk)
    form = SignForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('clinet.views.practical_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/sign/form.html', ctx)


@login_required_decorator
def sign_delete(request, pk):
    model = Sign.objects.get(id=pk)
    model.delete()
    return redirect('sign_list')


# ____________________________User Views_______________---

@login_required_decorator
def region_list(request):
    region = Region.objects.all()
    ctx = {
        'region': region,
        "we_active": 'active'
    }
    return render(request, 'dashboard/region/list.html', ctx)


@login_required_decorator
def region_create(request):
    model = Region()
    form = RegionForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('region_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/region/form.html', ctx)


@login_required_decorator
def region_edit(request, pk):
    model = Region.objects.get(id=pk)
    form = RegionForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('region_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/region/form.html', ctx)


@login_required_decorator
def region_delete(request, pk):
    model = get_object_or_404(Region, id=pk)
    model.delete()
    return redirect('region_list')


@login_required_decorator
def district_list(request):
    district = District.objects.all()
    ctx = {
        'district': district,
        "wr_active": 'active'
    }
    return render(request, 'dashboard/district/list.html', ctx)


@login_required_decorator
def district_create(request):
    model = District()
    form = DistrictForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('district_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/district/form.html', ctx)


@login_required_decorator
def district_edit(request, pk):
    model = District.objects.get(id=pk)
    form = DistrictForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('district_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/district/form.html', ctx)


@login_required_decorator
def district_delete(request, pk):
    model = District.objects.get(id=pk)
    model.delete()
    return redirect('district_list')


@login_required_decorator
def educationcategory_list(request):
    educationcategory = EducationCategory.objects.all()
    ctx = {
        'educationcategory': educationcategory,
        "wy_active": 'active'
    }
    return render(request, 'dashboard/edu/list.html', ctx)


@login_required_decorator
def educationcategory_create(request):
    model = EducationCategory()
    form = EducationCategoryForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('educationcategory_list')
        else:
            print(form.errors)
            # print(form, 'Salom')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/edu/form.html', ctx)


@login_required_decorator
def educationcategory_edit(request, pk):
    model = EducationCategory.objects.get(id=pk)
    form = EducationCategoryForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('educationcategory_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/edu/form.html', ctx)


@login_required_decorator
def educationcategory_delete(request, pk):
    model = EducationCategory.objects.get(id=pk)
    model.delete()
    return redirect('educationcategory_list')


@login_required_decorator
def list_schoool(request):
    maktab = User.objects.all()
    ctx = {
        'maktab': maktab,
        "wu_active": 'active'
    }
    return render(request, 'dashboard/maktab/list.html', ctx)


def school_create(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        school_form = SchoolForm(data=request.POST)
        if user_form.is_valid() and school_form.is_valid():
            user = user_form.save()
            school = school_form.save(False)
            school.user = user
            school.save()

            redirect("/")
        else:
            messages.warning(request, 'Please correct the errors below')
    else:
        user_form = UserForm()
        school_form = SchoolForm()
    return render(request, 'dashboard/maktab/form.html', {'user_form': user_form, 'school_form': school_form})


def get_model_or_none(model, pk):
    try:
        return model.objects.get(id=pk)
    except:
        return None

@login_required_decorator
def school_edit(request, pk: int):
    model = get_model_or_none(School, pk)
    if model:
        if request.method == 'POST':
            user_form = UserForm(data=request.POST, instance=School.director)
            school_form = SchoolForm(data=request.POST, instance=School)
            if user_form.is_valid() and school_form.is_valid():
                user = user_form.save()
                school = school_form.save(False)
                school.user = user
                school.save()

                redirect("/")
            else:
                messages.warning(request, 'Please correct the errors below')
        else:
            user_form = UserForm()
            school_form = SchoolForm()
        return render(request, 'dashboard/maktab/form.html', {'user_form': user_form, 'school_form': school_form})
    else:
        return HttpResponse("404 Not Found")

@login_required_decorator
def school_delete(request, pk):
    model = User.objects.get(id=pk)
    model.delete()
    return redirect('maktab_list')


@login_required_decorator
def group_list(request):
    group = Group.objects.all()
    ctx = {
        'group': group,
        "ww_active": 'active'
    }
    return render(request, 'dashboard/group/list.html', ctx)


@login_required_decorator
def group_create(request):
    model = Group()
    form = GroupForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('group_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'teachers':User.objects.filter(role='3')
    }
    return render(request, 'dashboard/group/form.html', ctx)


@login_required_decorator
def group_edit(request, pk):
    model = Group.objects.get(id=pk)
    form = GroupForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('group_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/group/form.html', ctx)


@login_required_decorator
def group_delete(request, pk):
    model = Group.objects.get(id=pk)
    model.delete()
    return redirect('group_list')


@login_required_decorator
def contact_list(request):
    contact = Contact.objects.all()
    ctx = {
        'contact': contact,
        "wq_active": 'active'
    }
    return render(request, 'dashboard/contact/list.html', ctx)


@login_required_decorator
def contact_create(request):
    model = Contact()
    form = ContactForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('contact_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
    }
    return render(request, 'dashboard/contact/form.html', ctx)


@login_required_decorator
def contact_edit(request, pk):
    model = Contact.objects.get(id=pk)
    form = ContactForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/contact/form.html', ctx)


@login_required_decorator
def contact_delete(request, pk):
    model = Contact.objects.get(id=pk)
    model.delete()
    return redirect('contact_list')


@login_required_decorator
def pay_list(request):
    pay = Pay.objects.all()
    ctx = {
        'pay': pay,
        "wm_active": 'active'
    }
    return render(request, 'dashboard/pay/list.html', ctx)


@login_required_decorator
def pay_create(request):
    model = Pay()
    form = PayForm(request.POST, request.FILES, instance=model)
    print(request.POST)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('pay_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'pupils':User.objects.filter(role='4')
    }
    return render(request, 'dashboard/pay/form.html', ctx)


@login_required_decorator
def pay_edit(request, pk):
    model = Pay.objects.get(id=pk)
    form = PayForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('pay_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/pay/form.html', ctx)


@login_required_decorator
def pay_delete(request, pk):
    model = Pay.objects.get(id=pk)
    model.delete()
    return redirect('pay_list')


@login_required_decorator
def referral_list(request):
    referral = Referral.objects.all()
    ctx = {
        'referral': referral,
        "wn_active": 'active'
    }
    return render(request, 'dashboard/referral/list.html', ctx)


@login_required_decorator
def referral_create(request):
    model = Referral()

    form = ReferralForm(request.POST, request.FILES, instance=model)

    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('referral_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'teachers':User.objects.filter(role='3'),
        'pupils':User.objects.filter(role='4'),

    }
    print('teachers')
    return render(request, 'dashboard/referral/form.html', ctx)


@login_required_decorator
def referral_edit(request, pk):
    model = Referral.objects.get(id=pk)
    form = ReferralForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('referral_list')
    ctx = {
        "form": form,
        'teachers':User.objects.filter(role='3'),
        'pupils':User.objects.filter(role='4'),
    }
    return render(request, 'dashboard/referral/form.html', ctx)


@login_required_decorator
def referral_delete(request, pk):
    model = Referral.objects.get(id=pk)
    model.delete()
    return redirect('referral_list')


@login_required_decorator
def attendance_list(request):
    attendance = Attendance.objects.all()
    ctx = {
        'attendance': attendance,
        "wb_active": 'active'
    }
    return render(request, 'dashboard/attendance/list.html', ctx)


@login_required_decorator
def attendance_create(request):
    model = Attendance()
    form = AttendanceForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'teachers':User.objects.filter(role='3'),
        'pupils':User.objects.filter(role='4')
    }
    return render(request, 'dashboard/attendance/form.html', ctx)


@login_required_decorator
def attendance_edit(request, pk):
    model = Attendance.objects.get(id=pk)
    form = AttendanceForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    ctx = {
        "form": form,
        'teachers': User.objects.filter(role='3'),
        'pupils': User.objects.filter(role='4')

    }
    return render(request, 'dashboard/attendance/form.html', ctx)


@login_required_decorator
def attendance_delete(request, pk):
    model = Attendance.objects.get(id=pk)
    model.delete()
    return redirect('attendance_list')


@login_required_decorator
def rating_list(request):
    rating = Rating.objects.all()
    ctx = {
        'rating': rating,
        "wv_active": 'active'
    }
    return render(request, 'dashboard/rating/list.html', ctx)


@login_required_decorator
def rating_create(request):
    model = Rating()
    form = RatingForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('rating_list')
        else:
            print(form.errors)
    ctx = {
        "form": form,
        'pupils':User.objects.filter(role='4'),
        'teachers':User.objects.filter(role='3')
    }
    return render(request, 'dashboard/rating/form.html', ctx)


@login_required_decorator
def rating_edit(request, pk):
    model = Rating.objects.get(id=pk)
    form = RatingForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('rating_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/rating/form.html', ctx)


@login_required_decorator
def rating_delete(request, pk):
    model = Rating.objects.get(id=pk)
    model.delete()
    return redirect('rating_list')


@login_required_decorator
def user_list(request):
    user = User.objects.all()
    ctx = {
        'users': user,
    }
    return render(request, 'dashboard/user/list.html', ctx)


@login_required_decorator
def user_create(request):
    model = User()
    form = UserForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/user/form.html', ctx)


@login_required_decorator
def user_edit(request, pk):
    model = User.objects.get(id=pk)
    form = UserForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('user_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/user/form.html', ctx)


@login_required_decorator
def user_delete(request, pk):
    model = User.objects.get(id=pk)
    model.delete()
    return redirect('user_list')


@login_required_decorator
def video_list(request):
    video = Video.objects.all()
    ctx = {
        'videos': video,
        "ww_active": 'active'

    }
    return render(request, 'dashboard/video/list.html', ctx)


@login_required_decorator
def video_create(request):
    model = Video()
    form = VideoForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('video_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/video/form.html', ctx)


@login_required_decorator
def video_edit(request, pk):
    model = Video.objects.get(id=pk)
    form = VideoForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('video_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/video/form.html', ctx)

@login_required_decorator
def video_delete(request, pk):
    model = Video.objects.get(id=pk)
    model.delete()
    return redirect('video_list')

# ==============================================================================================

@login_required_decorator
def category_list(request):
    categories = Category.objects.all()
    ctx = {
        'categories': categories,
    }
    return render(request, 'dashboard/category/list.html', ctx)


@login_required_decorator
def category_create(request):
    model = Category()
    form = CategoryForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('category_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_edit(request, pk):
    model = Category.objects.get(id=pk)
    form = CategoryForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('category_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/category/form.html', ctx)


@login_required_decorator
def category_delete(request, pk):
    model = Category.objects.get(id=pk)
    model.delete()
    return redirect('category_list')


@login_required_decorator
def subject_list(request):
    subjects = Subject.objects.all()
    ctx = {
        'subjects': subjects,
    }
    return render(request, 'dashboard/subject/list.html', ctx)


@login_required_decorator
def subject_create(request):
    model = Subject()
    form = SubjectForm(request.POST, request.FILES, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('subject_list')
        else:
            print(form.errors)
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/subject/form.html', ctx)


@login_required_decorator
def subject_edit(request, pk):
    model = Subject.objects.get(id=pk)
    form = SubjectForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    ctx = {
        "form": form
    }
    return render(request, 'dashboard/subject/form.html', ctx)


@login_required_decorator
def subject_delete(request, pk):
    model = Subject.objects.get(id=pk)
    model.delete()
    return redirect('subject_list')