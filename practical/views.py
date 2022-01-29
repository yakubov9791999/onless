from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from user.models import *
from practical.models import *


# Create your views here.
@login_required
def add_car(request):
    if request.user.role == '2':
        models = CarModel.objects.filter().order_by('title')
        regions = Region.objects.all().order_by('title')
        school = request.user.school
        instructors = User.objects.filter(role=6, school=school)
        # print(instructors)
        context = {
            'models': models,
            'regions': regions,
            'instructors': instructors,
        }
        return render(request, 'practical/add_car.html', context)

        # instructor = User.objects.filter(school=request.user.school)
        # print(request.user)
