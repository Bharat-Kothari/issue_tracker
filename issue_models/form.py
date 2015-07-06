from django import forms
from django.forms import ModelMultipleChoiceField
from issue_models.models import MyUser, new_project
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
class SignupForm(forms.ModelForm):
    password=forms.CharField(label="password",widget=forms.PasswordInput())
    confirm_password=forms.CharField(label="confirm password",widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['emailaddr', 'first_name', 'last_name', 'dob', 'photo', 'password']
    error_messages = {
        'password_mismatch':("password mismatch"),
    }

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password= self.cleaned_data.get("confirm_password")
        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code='password_mismatch')

        # Always return the cleaned data, whether you have changed it or
        # not.

        return confirm_password

    def save(self, commit=True):
            user = super(SignupForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user

class LoginForm(forms.Form):
    emailaddr= forms.EmailField(label="email address")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch':("invalid username or password"),
    }
    def clean_password(self):
        password = self.cleaned_data.get("password")
        emailaddr= self.cleaned_data.get("emailaddr")
        user = authenticate(emailaddr=emailaddr, password=password)
        if user is None:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code='password_mismatch')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields = ['first_name', 'last_name', 'dob', 'photo',]


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model=new_project
        fields = ['projtitle', 'description', 'Assigned_to']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['Assigned_to'].widget = forms.CheckboxSelectMultiple()
        self.fields["Assigned_to"].queryset = MyUser.objects.all()


    def save(self, commit=True):
            print 'abc'
            user1 = super(CreateProjectForm, self).save(commit=False)
            user1.projectmanager = self.request.user
            print 'abc1'
            user1.save()
            self.save_m2m();