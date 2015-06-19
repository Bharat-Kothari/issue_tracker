from django import forms

# class SignupInfoForm(forms.Form):
#     emailaddress = forms.EmailField()
#     password = forms.PasswordInput()
#     first_name = forms.CharField(max_length=100)
#     last_name =  forms.CharField(max_length=30)
#     dob = forms.DateField()
#
from django import forms
from issue_models.models import MyUser

class SignupForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['emailaddr', 'password', 'first_name', 'last_name', 'dob']
