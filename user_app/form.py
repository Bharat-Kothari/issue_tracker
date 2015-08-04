from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate

from user_app.models import MyUser


class SignupForm(forms.ModelForm):

    """
    Form for signup
    To Create New User
    """
    # redefining password for adding minimum length and regex
    password = forms.CharField(label="password", min_length=6, widget=forms.PasswordInput(),
                               validators=[RegexValidator(regex='(?=.*[0-9])(?=.*[!@#$%^&*()-+])',
                                                          message="password should have a number and special symbol")])
    confirm_password = forms.CharField(label="confirm password", min_length=6, widget=forms.PasswordInput())

    class Meta:

        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'dob', 'photo', 'password']

    error_messages = {
        'password_mismatch': "password mismatch",
    }

    # To check the entered password matches or not
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code='password_mismatch')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print email
        try:
            email_check = MyUser.objects.get(email__iexact=email)
        except:
            email_check = False

        if email_check:
            raise forms.ValidationError("Email id already exists")
        return email

    def save(self, commit=True):
            user = super(SignupForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user


class LoginForm(forms.Form):
    """
    Login form to take email and password from user and authenticate

    """
    email = forms.EmailField(label="email address")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    error_messages = {
        'invalid_user': "invalid username or password",
    }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        email_check = MyUser.objects.get(email__iexact=email)
        print email_check.email
        user = authenticate(email=email_check.email, password=password)
        print user
        if user is None:
            raise forms.ValidationError(
                self.error_messages["invalid_user"],
                code='invalid_user')
        return password


class ProfileUpdateForm(forms.ModelForm):
    """
    Profile update form
    """
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'dob', 'photo', ]


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput, min_length=6,
                                    validators=[RegexValidator(regex='(?=.*[0-9])(?=.*[!@#$%^&*()-+])',
                                                               message="enter password having number and symbol")])
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput, min_length=6,
                                    validators=[RegexValidator(regex='(?=.*[0-9])(?=.*[!@#$%^&*()-+])',
                                                               message="enter password having number and symbol")])