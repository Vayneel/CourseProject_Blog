from django import forms
from user_app.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserAuthForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class UserAdditionalForm(forms.ModelForm):
    class Meta:
        model = UserAdditional
        fields = ['avatar', 'birthday']
