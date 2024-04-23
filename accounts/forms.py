from typing import Any
from django import forms
from .models import Accounts

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'placeholder' : 'Enter Password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs= {
        'placeholder' : 'Confirm Password',
        'class': 'form-control'
    }))
    choices = [('M','Male'),('F','Female'),('O','Others')]
    gender=forms.CharField( widget=forms.RadioSelect(choices=choices), initial='M')

    class Meta():
        model   = Accounts
        fields  = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'gender'] 
    
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['gender'].widget.attrs['class'] = 'custom-control-input'
        for field in self.fields:
            if field != 'gender':
                self.fields[field].widget.attrs['class'] = 'form-control'
    
    def clean(self) -> dict[str, Any]:
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm Password should be match')


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
     
    class Meta():
        model = Accounts
        fields = ['email', 'password',]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'