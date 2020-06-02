from django import forms
from user.models import User

class AuthenticationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('role', 'driving_school', 'is_staff')