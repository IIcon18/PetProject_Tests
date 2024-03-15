from django import  forms
class loginform(forms.Form):
    name= forms.CharField(max_length=100)
    passw = forms.CharField(max_length=100)