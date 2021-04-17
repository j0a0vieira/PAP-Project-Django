from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Username'}))
    password1= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Password', 'type':'password'}))
    password2= forms.CharField(max_length=100,
                           widget= forms.TextInput
                           (attrs={'placeholder':'Re-enter your password', 'type':'password'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
