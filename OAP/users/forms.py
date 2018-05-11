from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields =("username",)

class LoginForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        fiels = ()