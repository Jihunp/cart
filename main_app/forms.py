# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=3, max_length=120)
    email = forms.EmailField(label='Enter Email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 =  forms.CharField(label= 'Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        u = User.objects.filter(username=username)
        if u.count():
            raise ValidationError("Username has been used")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = User.objects.filter(email=email)
        if u.count():
            raise ValidationError("Email has been used")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password does not match")

        return password2

    def save_login(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user