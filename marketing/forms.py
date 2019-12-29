from django import forms
from marketing.models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'type': 'email',
        'name': 'email',
        'id': 'email',
        'placeholder': 'type your email address',
    }), label="")

    class Meta:
        model = Signup
        fields = ('email',)
