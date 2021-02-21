from django import forms

from sign.models import *


class AddScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ( 'date', 'subject', 'theme',)
        exclude = ['',]


# class AddSubjectForm(forms.ModelForm):
#     class Meta:
#         model = Subject
#         fields = ['title','sort', 'category']
#         exclude = ['created_date', 'is_active', 'school', 'author']

# class UpdateScheduleForm(forms.ModelForm):
#
#     class Meta:
#         model = Schedule
#         fields = ('start','stop', 'sort',)
#         exclude = ['subject','theme','date',]


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