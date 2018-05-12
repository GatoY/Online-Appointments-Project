from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import User, userInfo
from django.core.validators import RegexValidator


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)


class LoginForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        fields = ()


class InfoForm(forms.ModelForm):
    # address = forms.CharField(max_length=80)
    # mobile = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    # error_message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # workPhone = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    # error_message="workPhone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # home = forms.RegexField(regex=r'^\+?1?\d{9,15}$')
    # error_message="Home number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    class Meta:
        model = userInfo
        fields = ['address','mobile', 'workPhone', 'home']