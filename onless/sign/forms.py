from django import forms

from sign.models import *


class AddScheduleFrom(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Fan nomi", queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Mavzu nomi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    sort = forms.IntegerField(label='Tartibi',
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '3', }))
    class Meta:
        model = Schedule
        fields = ('subject', 'title', 'sort')
        exclude = ('author',)


class AddSubjectFrom(forms.ModelForm):
    category = forms.ChoiceField(label="Toifasi", choices=CATEGORY_CHOICES,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    title = forms.CharField(label='Fan nomi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    sort = forms.IntegerField(label='Tartibi',
                               widget=forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '3', }))

    class Meta:
        model = Subject
        fields = ('category', 'title', 'sort')

