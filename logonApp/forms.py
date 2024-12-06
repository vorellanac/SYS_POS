from django import forms  
from django.contrib.auth.forms import UserCreationForm  
from .models import CustomUser  

class CustomUserCreationForm(UserCreationForm):  
    class Meta:  
        model = CustomUser  
        fields = ('username', 'email', 'password1', 'password2', 'user_type')  

class CustomUserLoginForm(forms.Form):  
    username = forms.CharField(max_length=150)  
    password = forms.CharField(widget=forms.PasswordInput) 