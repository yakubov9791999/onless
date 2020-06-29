from allauth.account.forms import SetPasswordField, PasswordField
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.forms import ModelForm
from user.models import *
from django import forms


class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'school', 'is_staff')


class AddUserForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'phone',)
        exclude = ('username', 'password', 'school', 'pasport')


class AddPupilForm(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'phone', 'group')
        exclude = ('username', 'password', 'school', 'pasport', 'birthday')


class AddGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('number', 'teacher', 'start', 'stop', 'category', 'price')
        exclude = ('school',)


class AddTeacherGroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('number', 'start', 'stop', 'category', 'price')
        exclude = ('school', 'teacher')


class GroupUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['teacher'].queryset = User.objects.filter(Q(role=3, school=user.school)|Q(role=2, school=user.school))



    number = forms.IntegerField(label="Raqami", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(label="O'quv yili", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    teacher = forms.ModelChoiceField(label="O'qituvchi", queryset=User.objects.filter(role=3),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    start = forms.DateField(label="O'qish boshlanishi", widget=forms.DateInput(attrs={'class': 'form-control'}))
    stop = forms.DateField(label="O'qish tugashi", widget=forms.DateInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(label="Toifasi", choices=CATEGORY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label="O'qish summasi", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sort = forms.IntegerField(label='Tartibi', widget=forms.NumberInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Group
        fields = ('category', 'number', 'year', 'teacher', 'start', 'stop', 'price', 'sort')


class EditUserForm(ModelForm):
    name = forms.CharField(label='F.I.O', widget=forms.TextInput(attrs={'class': 'form-control'}))
    region = forms.ModelChoiceField(label="Viloyat", queryset=Region.objects.all(),
                                    widget=forms.Select(
                                        attrs={'class': 'form-control', 'id': 'region', 'required': 'required'}))
    district = forms.ModelChoiceField(label="Tuman/Shahar", queryset=District.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': 'form-control', 'id': 'district', 'required': 'required'}))
    avatar = forms.ImageField(label='Rasm', widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    birthday = forms.DateField(label="Tug'ilgan kun", widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='Tel raqam',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '9', }))
    gender = forms.ChoiceField(label='Jinsi', choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    turbo = forms.CharField(label='Parol', widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Pasport', widget=forms.TextInput(attrs={'class': 'form-control', }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pasport'].disabled = True
        # self.fields['pasport'].widget.attrs['readonly'] = True

    def clean_turbo(self):
        turbo = self.cleaned_data['turbo']
        return turbo

    class Meta:
        model = User
        fields = ('name', 'pasport', 'region', 'district', 'avatar', 'birthday', 'phone', 'gender', 'turbo',)


class EditPupilForm(ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(school=request.user.school)


    name = forms.CharField(label='F.I.O', widget=forms.TextInput(attrs={'class': 'form-control'}))
    region = forms.ModelChoiceField(label="Viloyat", queryset=Region.objects.all(),
                                    widget=forms.Select(
                                        attrs={'class': 'form-control', 'id': 'region', 'required': 'required'}))
    district = forms.ModelChoiceField(label="Tuman/Shahar", queryset=District.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': 'form-control', 'id': 'district', 'required': 'required'}))
    birthday = forms.DateField(label="Tug'ilgan kun", widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='Tel raqam',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '9', }))
    gender = forms.ChoiceField(label='Jinsi', choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    turbo = forms.CharField(label='Parol', widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Pasport', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pasport'}))
    group = forms.ModelChoiceField(label='Guruh',queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('name', 'pasport','group', 'region', 'district', 'birthday', 'phone', 'gender', 'turbo')

class EditWorkerForm(ModelForm):
    name = forms.CharField(label='F.I.O', widget=forms.TextInput(attrs={'class': 'form-control'}))
    region = forms.ModelChoiceField(label="Viloyat", queryset=Region.objects.all(),
                                    widget=forms.Select(
                                        attrs={'class': 'form-control', 'id': 'region', 'required': 'required'}))
    district = forms.ModelChoiceField(label="Tuman/Shahar", queryset=District.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': 'form-control', 'id': 'district', 'required': 'required'}))
    birthday = forms.DateField(label="Tug'ilgan kun", widget=forms.DateInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='Tel raqam',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '9', }))
    gender = forms.ChoiceField(label='Jinsi', choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    turbo = forms.CharField(label='Parol', widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Pasport', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pasport'}))

    class Meta:
        model = User
        fields = ('name', 'pasport', 'region', 'district', 'birthday', 'phone', 'gender', 'turbo')

class EditSchoolForm(ModelForm):
    # def __init__(self, *args, user=None, **kwargs, ):
    #     super().__init__(*args, **kwargs,)
    #     if user:
    #         self.fields['district'].queryset = self.fields['district'].queryset.filter(region=user.school.region)

    title = forms.CharField(label="Nomi", widget=forms.TextInput(attrs={'class': 'form-control'}))
    director = forms.ModelChoiceField(label="Rahbar nomi", queryset=User.objects.filter(role=2),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Tel raqam", widget=forms.TextInput(attrs={'class': 'form-control'}))
    logo = forms.ImageField(label="Rasm", widget=forms.FileInput(attrs={'class': 'form-control'}), required=False)
    region = forms.ModelChoiceField(label="Viloyat", queryset=Region.objects.all(),
                                    widget=forms.Select(
                                        attrs={'class': 'form-control', 'id': 'region', 'required': 'required'}))
    district = forms.ModelChoiceField(label="Tuman/Shahar", queryset=District.objects.all(),
                                      widget=forms.Select(
                                          attrs={'class': 'form-control', 'id': 'district', 'required': 'required'}))

    class Meta:
        model = School
        fields = ('title', 'director', 'phone', 'logo', 'region', 'district')


class AddContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'text')
        exclude = ('photo',)
