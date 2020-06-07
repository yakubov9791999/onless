from allauth.account.forms import SetPasswordField, PasswordField
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import User, Group, GENDER_CHOICES
from django import forms
class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'school', 'is_staff')


class AddUserForm(ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = User
        fields = ('name', 'address', 'phone', 'birthday',)
        exclude = ('gender', 'username', 'password', 'school')

class AddGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('number', 'year', 'teacher', 'start', 'stop', 'category')
        exclude = ('school',)


class EditUserForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '9',}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'address', 'avatar', 'birthday', 'phone', 'gender')


# class EditSchoolForm(ModelForm):



