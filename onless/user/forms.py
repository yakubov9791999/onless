from allauth.account.forms import SetPasswordField, PasswordField
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
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
    def clean(self):
        start = self.cleaned_data['start']
        stop = self.cleaned_data['stop']

        if stop < start:
            raise ValidationError("Guruh boshlanish vaqti tugash vaqtidan oldin bo'lishi mumkin emas")

    class Meta:
        model = Group
        fields = ('number', 'teacher', 'start', 'stop', 'category',)
        exclude = ('school', 'price')




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

    def clean(self):
        start = self.cleaned_data['start']
        stop = self.cleaned_data['stop']

        if stop < start:
            raise ValidationError("Guruh boshlanish vaqti tugash vaqtidan oldin bo'lishi mumkin emas")

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
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'max': '999999999','id': 'phone' }))
    gender = forms.ChoiceField(label='Jinsi', choices=GENDER_CHOICES,
                               widget=forms.Select(attrs={'class': 'form-control'}))
    turbo = forms.CharField(label='Parol', widget=forms.TextInput(attrs={'class': 'form-control'}))
    pasport = forms.CharField(label='Pasport', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'pasport'}))
    group = forms.ModelChoiceField(label='Guruh',queryset=Group.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    place_of_birth = forms.CharField(label='Tug\'ilgan joyi)',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Masalan: Samarqand v. Urgut t.','id': 'place_of_birth'}))
    residence_address = forms.CharField(label='Yashash manzili (Propiska bo\'yicha)', required=False,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Alpomish MFY Fayzobod 1A 53/26 ', 'id': 'residence_address', 'required': False,}))
    passport_issued_time = forms.CharField(label='Amal qilish muddati (fuqarolik pasporti)',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date','id': 'passport_issued_time', 'required': False,}))
    passport_issued_organization = forms.CharField(label='Kim tomonidan berilgan (fuqarolik pasporti)',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Buxoro viloyati Kogon tumani IIB','required': False, 'id': 'passport_issued_organization'}))
    medical_series = forms.CharField(label='Tibbiy ma\'lumotnoma seriyasi (0.83 med spravka)',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 00859545','required': False, 'id': 'medical_series'}))
    medical_issued_organization = forms.CharField(label='Tibbiy ma\'lumotnoma bergan tashkilot (poliklinika)',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Yunusobod tuman poliklinikasi','required': False, 'id': 'medical_issued_organization'}))
    medical_issued_date = forms.CharField(label='Tibbiy ma\'lumotnoma berilgan sana',  required=False, widget=forms.TextInput(attrs={'class': 'form-control','type':'date','required': False, 'id': 'medical_issued_organization'}))
    certificate_series = forms.CharField(label='Guvohnoma seriyasi',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 10 AA','required': False, 'id': 'certificate_series'}))
    certificate_number = forms.CharField(label='Guvohnoma raqami',  required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: 316561','required': False, 'id': 'certificate_number'}))

    class Meta:
        model = User
        fields = ('name', 'pasport','group', 'region', 'district', 'birthday', 'phone', 'gender', 'turbo', 'place_of_birth', 'residence_address', 'passport_issued_time', 'passport_issued_organization', 'medical_series', 'medical_issued_organization', 'medical_issued_date','certificate_number', 'certificate_series')

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
        fields = ('title', 'phone', 'logo', 'region', 'district')


class AddContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ( 'text',)
        exclude = ('user','photo',)


class SendSmsForm(ModelForm):
    class Meta:
        model = Sms
        fields = ('text', )
