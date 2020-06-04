from allauth.account.forms import SetPasswordField, PasswordField
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import User
from django import forms
class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'driving_school', 'is_staff')


class AddUserForm(ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = User
        fields = ('name', 'address', 'phone', 'birthday',)
        exclude = ('gender', 'username', 'password', 'driving_school')








