from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Hobby

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=False)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'name', 'date_of_birth', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)