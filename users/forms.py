from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.models import Profile


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Form definition for UserUpdate."""

    class Meta:
        """Meta definition for UserUpdateform."""

        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    """Form definition for ProfileUpdate."""

    class Meta:
        """Meta definition for ProfileUpdateform."""

        model = Profile
        fields = ('image',)
