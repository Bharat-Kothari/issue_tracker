from django import forms
from issue_models.models import MyUser
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

