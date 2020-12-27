from django import forms

from sign.models import *


class AddScheduleForm(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Fan nomi", queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'subject'}))
    theme = forms.CharField(label='Mavzu nomi', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Ogohlantiruvchi belgilar'}))
    sort = forms.IntegerField(label='Tartibi',
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'max': '999', 'placeholder': 'Masalan: 1'}))
    class Meta:
        model = Schedule
        fields = ( 'start', 'stop', 'sort',)
        exclude = ['subject','theme', 'date', ]


# class AddSubjectForm(forms.ModelForm):
#     class Meta:
#         model = Subject
#         fields = ['title','sort', 'category']
#         exclude = ['created_date', 'is_active', 'school', 'author']

class UpdateScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ('start','stop', 'sort',)
        exclude = ['subject','theme','date',]


# class UpdateSubjectForm(forms.ModelForm):
#
#     class Meta:
#         model = Subject
#         fields = ['title', 'sort', 'category']
#         exclude = ['created_date', 'is_active', 'school', 'author',]


class AddMaterialFrom(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'file')
        exclude = ('video', 'school' )