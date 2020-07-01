from django import forms

from sign.models import *


class AddScheduleFrom(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Fan nomi", queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'subject'}))
    title = forms.CharField(label='Mavzu nomi', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masalan: Ogohlantiruvchi belgilar'}))
    sort = forms.IntegerField(label='Tartibi',
                              widget=forms.NumberInput(attrs={'class': 'form-control', 'max': '999', 'placeholder': 'Masalan: 1'}))
    class Meta:
        model = Schedule
        fields = ('subject', 'title', 'sort')
        exclude = ('author',)

class UpdateScheduleForm(forms.ModelForm):
    subject = forms.ModelChoiceField(label="Fan nomi", queryset=Subject.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control', 'id': 'subject'}))
    title = forms.CharField(label='Mavzu nomi', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Masalan: Ogohlantiruvchi belgilar'}))
    sort = forms.IntegerField(label='Tartibi',
                              widget=forms.NumberInput(
                                  attrs={'class': 'form-control', 'max': '999', 'placeholder': 'Masalan: 1'}))

    class Meta:
        model = Schedule
        fields = ('subject', 'title', 'sort')

class AddMaterialFrom(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('title', 'file')
        exclude = ('video', 'school' )