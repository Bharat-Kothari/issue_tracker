from django import forms
from django.core.mail import send_mail
from django.forms import BaseFormSet

from Issue_Track import settings
from issue_tracker.models import MyUser, Project, Story


class CreateProjectForm(forms.ModelForm):

    """
    # Create Project Form
    """
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


class UpdateProjectForm(forms.ModelForm):
    """
    Update project Form
    """
    class Meta:
        model = Project
        fields = ['project_title', 'description', 'assigned_to']

    # To pop the request send from view and set member field
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.id = kwargs.pop('id')
        super(UpdateProjectForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].widget = forms.CheckboxSelectMultiple()
        self.fields["assigned_to"].queryset = MyUser.objects.exclude(email=self.request.user)

    # To save the modified Project and send mail to new member
    def save(self, commit=True):
            temp = Project.objects.get(id=self.id)
            old_list = temp.assigned_to.all()
            user1 = super(UpdateProjectForm, self).save(commit=False)
            new_list = self.cleaned_data['assigned_to']
            subject = user1.project_title
            message = ' You have been added in the project'
            from_email = settings.EMAIL_HOST_USER
            new = new_list.exclude(pk__in=old_list)
            for assigned_user in new:
                    to_mail = assigned_user.email
                    send_mail(subject, message, from_email, [to_mail], fail_silently=True)

            user1.save()
            self.save_m2m()
            user1.assigned_to.add(self.request.user)

            return user1


class ProjectForm(forms.ModelForm):
    """
    Form for Project creation
    """
    model = Project
    fields = ['project_title', 'description', 'assigned_to']


class UpdateStoryForm(forms.ModelForm):
    """
    Form to update a story
    """
    class Meta:
        model = Story
        fields = ['story_title', 'description', 'assignee', 'estimate', 'scheduled', 'status']
    error_messages = {
        'unscheduled': "This has to be un-started when story is not scheduled",
    }

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(UpdateStoryForm, self).__init__(*args, **kwargs)
        story = Story.objects.get(pk=self.id)
        project = story.project_title
        self.fields['assignee'].queryset = project.assigned_to.all()

    # To check user have not scheduled and done status other than un-started
    def clean_status(self):
        assignee = self.cleaned_data.get("assignee")
        status = self.cleaned_data.get("status")
        scheduled = self.cleaned_data.get("scheduled")
        if scheduled == 'no' and status != 'unstrtd':
            raise forms.ValidationError(self.error_messages["unscheduled"], code='unscheduled')

        if assignee==None and status != 'unstrtd':
            raise forms.ValidationError("Assignee need to assigned when status is other than unstarted ")

        return status

    def clean_estimate(self):
        estimate = self.cleaned_data.get("estimate")
        if estimate >100:
            raise forms.ValidationError("Enter value less than 100")
        return estimate

class AddStoryForm(forms.ModelForm):
    description = forms.CharField(max_length=500, required=False)
    estimate = forms.IntegerField(required=False)

    class Meta:
        model = Story
        fields = ['story_title', 'description', 'assignee', 'estimate', 'scheduled']

    def __init__(self, *args, **kwargs):
        id = kwargs.pop('id')
        super(AddStoryForm, self).__init__(*args, **kwargs)
        project = Project.objects.get(pk=id)
        self.fields['assignee'].queryset = project.assigned_to.all()

    def clean_estimate(self):
        estimate = self.cleaned_data.get("estimate")
        if estimate >100:
            raise forms.ValidationError("Enter value less than 100")
        return estimate

class AddStoryFormSet(BaseFormSet):

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('id')
        super(AddStoryFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['id'] = self.id
        return super(AddStoryFormSet, self)._construct_form(i, **kwargs)