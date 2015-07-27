from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth import authenticate
from django.forms import modelformset_factory, BaseFormSet

from Issue_Track import settings
from issue_models.models import MyUser, Project, Story


# Form for signup
class SignupForm(forms.ModelForm):
    # redefining password
    password = forms.CharField(label="password",min_length=6, widget=forms.PasswordInput(),
            validators=[RegexValidator(regex ='(?=.*[0-9])(?=.*[!@#$%^&*()-+])', message="enter proper password")])
    confirm_password = forms.CharField(label="confirm password", min_length=6, widget=forms.PasswordInput())

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'dob', 'photo', 'password']
    error_messages = {
        'password_mismatch': ("password mismatch"),
    }

    # To check the entered password matches or not
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password =  self.cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code='password_mismatch')
        return confirm_password

    def save(self, commit=True):
            user = super(SignupForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
            return user


# Login form to take email and password from user and authenticate
class LoginForm(forms.Form):

    email = forms.EmailField(label="email address")
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    error_messages = {
        'invalid_user': ("invalid username or password"),
    }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError(
                self.error_messages["invalid_user"],
                code='invalid_user')
        return password


# Profile update form
class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'dob', 'photo', ]


# Create Project Form
class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_title', 'description', 'assigned_to']

    # To pop the request send from view and set member field
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CreateProjectForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()
        self.fields["assigned_to"].queryset = MyUser.objects.exclude(email=self.request.user)

    # To save the project manager and send mail to project member
    def save(self, commit=True):
            user1 = super(CreateProjectForm, self).save(commit=False)
            user1.project_manager = self.request.user
            user1.save()
            self.save_m2m()
            subject = user1.project_title
            message = ' You have been added in the project'
            from_email = settings.EMAIL_HOST_USER
            for assigned_user in user1.assigned_to.all():
                to_mail = assigned_user.email
                send_mail(subject, message, from_email, [to_mail], fail_silently=True)
            user1.assigned_to.add(self.request.user)

            return user1


# Update project Form
class UpdateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['project_title', 'description', 'assigned_to']

    # To pop the request send from view and set member field
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.id = kwargs.pop('id')
        super(UpdateProjectForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()
        self.fields["assigned_to"].queryset = MyUser.objects.all()

    # To save the modified Project and send mail to new member
    def save(self, commit=True):
            temp = Project.objects.get(id=self.id)
            oldlist=temp.assigned_to.all()
            user1 = super(UpdateProjectForm, self).save(commit=False)
            newlist = self.cleaned_data['assigned_to']
            subject = user1.project_title
            message = ' You have been added in the project'
            from_email = settings.EMAIL_HOST_USER
            new= newlist.exclude(pk__in=oldlist)
            for assigned_user in new:
                    to_mail = assigned_user.email
                    send_mail(subject, message, from_email, [to_mail], fail_silently=True)

            user1.save()
            self.save_m2m()

            return user1


# Form for Project creation
class ProjectForm(forms.ModelForm):
    model = Project
    fields = ['project_title', 'description', 'assigned_to']



class UpdateStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story_title', 'description', 'assignee', 'estimate', 'scheduled', 'status']
    error_messages = {
        'unscheduled': ("This has to be unstarted when story is not scheduled"),
    }

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(UpdateStoryForm, self).__init__(*args, **kwargs)
        story = Story.objects.get(pk=self.id)
        project= story.project_title
        self.fields['assignee'].queryset = project.assigned_to.all()

    # To check user have not scheduled and done status other than unstarted
    def clean_status(self):
        status = self.cleaned_data.get("status")
        scheduled = self.cleaned_data.get("scheduled")
        assignee = self.cleaned_data.get("assignee")
        if scheduled == 'no' and status != 'unstrtd':
            raise forms.ValidationError(
            self.error_messages["unscheduled"],
            code='unscheduled')
        if assignee == None and status != 'unstrtd':
            raise forms.ValidationError("Assignee need to assigned when status is other than unstarted ")
        return status

class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput, min_length=6,validators=[RegexValidator(regex ='(?=.*[0-9])(?=.*[!@#$%^&*()-+])', message="enter proper password")])
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput, min_length=6,validators=[RegexValidator(regex ='(?=.*[0-9])(?=.*[!@#$%^&*()-+])', message="enter proper password")])




class AddStoryForm(forms.ModelForm):
    description = forms.CharField(max_length=500,required=False)
    estimate = forms.IntegerField("in hours",required=False)

    class Meta:
        model = Story
        fields = ['story_title', 'description', 'assignee', 'estimate', 'scheduled']

    def __init__(self,*args,**kwargs):
        id = kwargs.pop('id')
        super(AddStoryForm,self).__init__(*args,**kwargs)
        project = Project.objects.get(pk=id)
        self.fields['assignee'].queryset = project.assigned_to.all()

class AddStoryFormSet(BaseFormSet):
    def __init__(self, *args,**kwargs):
        self.id = kwargs.pop('id')
        super(AddStoryFormSet,self).__init__(*args,**kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['id']=self.id
        return super(AddStoryFormSet,self)._construct_form(i, **kwargs)

