from django import forms

class LoginForm(forms.Form):
       username = forms.CharField(max_length=100)
       password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
       username = forms.CharField(max_length=100)
       email = forms.EmailField()
       password = forms.CharField(widget=forms.PasswordInput)
   
