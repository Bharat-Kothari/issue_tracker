from django import forms

class LoginInfoForm(forms.Form):
    EmailAddress = forms.EmailField()
    Password=forms.PasswordInput()
