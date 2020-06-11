from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from sign.models import *


@login_required
def sign(request):
    signs = Sign.objects.all()
    return render(request, 'sign/signs.html', {
        'signs': signs,
    })
