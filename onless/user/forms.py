from allauth.account.forms import SetPasswordField, PasswordField
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import *
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

class GroupUpdateForm(ModelForm):
    number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(role=3), widget=forms.Select(attrs={'class': 'form-control'}))
    start = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    stop = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Group
        fields = ('number', 'year', 'teacher', 'start', 'stop', 'category')

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


class EditSchoolForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    director_fio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    district = forms.ModelChoiceField(queryset=District.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = School
        fields = ('title', 'director_fio', 'phone', 'logo', 'region', 'district')

class AddContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'text')
        exclude = ('photo',)