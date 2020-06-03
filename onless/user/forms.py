from django.forms import ModelForm
from user.models import User
from django import forms
class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'driving_school', 'is_staff')


class AddTeacher(ModelForm):

    gender = forms.CharField()

    class Meta:
        model = User
        fields = ('name', 'address', 'phone', 'birthday',)
        exclude = ('gender',)
