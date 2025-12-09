from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Device

class UserregistrationForm(UserCreationForm):

    email = forms.EmailField(required= True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_id', 'name', 'location' ]