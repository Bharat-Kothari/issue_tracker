from django import forms

# class SignupForm(forms.Form):
#     emailaddress = forms.EmailField()
#     password = forms.PasswordInput()
#     confirm_password = forms.PasswordInput()
#     first_name = forms.CharField(max_length=100)
#     last_name =  forms.CharField(max_length=30)
#     dob = forms.DateField()
# #
from django import forms
from issue_models.models import MyUser

class SignupForm(forms.ModelForm):
    confirm_password=forms.CharField(label="confirm password",widget=forms.PasswordInput())
    class Meta:
        model = MyUser
        fields = ['emailaddr', 'first_name', 'last_name', 'dob', 'password']

    def save(self, commit=True):
            user = super(SignupForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user


from django.contrib.auth import authenticate
from issue_models.models import MyUser


class LoginForm(forms.Form):
        emailaddr = forms.EmailField()
        password=forms.CharField(label="password",widget=forms.PasswordInput())

        def clean_emailaddr(self):
            data = self.cleaned_data['emailaddr']
            if  'emailaddr' not in data:
                raise forms.ValidationError("You have forgotten about Fred!")

        # Always return the cleaned data, whether you have changed it or
        # not.
            return data



        def clean_password(self):
            data = self.cleaned_data['password']
            if not data:
                raise forms.ValidationError(("Please enter your password"))
                return data


        def clean(self):
            try:
                emailaddr = MyUser.objects.get(emailaddr__iexact=self.cleaned_data['emailaddr']).emailaddr

            except MyUser.DoesNotExist:
                raise forms.ValidationError("No such email registered")
                password = self.cleaned_data['password']

                self.user = auth.authenticate(emailaddr=emailaddr, password=password)
                if self.emailaddr1 is None or not self.emailaddr1.is_active:
                    raise forms.ValidationError(("Email or password is incorrect"))
                    return self.cleaned_data

        # user = authenticate(emailaddr='emailaddr', password='password')
        # if user is not None:
        #     # the password verified for the user
        #     if user.is_active:
        #         print("User is valid, active and authenticated")
        #     else:
        #         print("The password is valid, but the account has been disabled!")
        # else:
        #     # the authentication system was unable to verify the username and password
        #     print("The username and password were incorrect.")