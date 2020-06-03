from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from user.models import User
from django import forms
class AuthenticationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'driving_school', 'is_staff')


class AddTeacher(ModelForm):

    gender = forms.CharField()

    class Meta:
        model = User
        fields = ('name', 'address', 'phone', 'birthday',)
        exclude = ('gender', 'username', 'password', 'driving_school')







    # def clean_password2(self):
    #     '''
    #     we must ensure that both passwords are identical
    #     '''
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError('Passwords must match')
    #     return password2