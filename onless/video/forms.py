from django import forms
from video.models import *



class AddVideoForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    video = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Video
        fields = ('title', 'video', 'photo')
        exclude = ('category',)


class SignUpSchoolForm(forms.ModelForm):

    class Meta:
        model = SignUpSchool
        fields = ['name', 'select', 'phone','district', 'tuman', 'text']
        exclude = ['region','district']