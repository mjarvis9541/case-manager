from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    class Meta:
        model = User
        fields = ['username']


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on the user, but
    replaces the password field with admin's password hash display field.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser']


class UserRegistrationForm(UserCreationForm):
    #full_name = forms.CharField(label='Full Name')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]

    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'placeholder': ''}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': ''}))

    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     try:
    #         User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise forms.ValidationError("The username you have entered does not exist.")
    #     return username

    # def clean(self, *args, **kwargs):
    #     cleaned_data = self.cleaned_data
    #     username = cleaned_data.get('username')
    #     password = cleaned_data.get('password')
    #     if username and password:
    #         user = authenticate(username=username, password=password)
    #         if not user:
    #             raise forms.ValidationError('Incorrect username/password.')
    #     return cleaned_data


class StaffCreationForm(UserCreationForm):
    username = forms.CharField(label='Staff ID')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'department', 'email', ]