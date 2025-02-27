from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from apps.authentication.models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = CustomUser
        fields = ('name', 'email', 'password1', 'password2')
        
class SignInForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')