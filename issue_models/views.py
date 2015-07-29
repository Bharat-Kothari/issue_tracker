from itertools import izip
import json
import operator
import datetime

from django.core.urlresolvers import reverse_lazy, reverse
from django.forms import modelformset_factory, formset_factory
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q, Sum
import time

from Issue_Track import settings
from issue_models.form import AddStoryFormSet, AddStoryForm
from issue_models.models import MyUser, Project, Story
from issue_models import form
from issue_models import tasks
# To check user is already logged in.


def login_check(f):
    def check_authentication(request, *args):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
        else:
            return f(request)

    return check_authentication


# To check user has logged in.


def logout_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request, *args, **kwargs)
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check a login member is member of that project


def project_member_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if Project.objects.filter(pk=kwargs['pk']).exists():
                project = Project.objects.get(id=kwargs['pk'])
                temp = project.assigned_to.all()
                if temp.filter(email=request.user.email):
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            else:
                raise Http404
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check that a project which is being updated,is updated by the Project manager


def project_update_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if Project.objects.filter(pk=kwargs['pk']).exists():
                project = Project.objects.get(id=kwargs['pk'])
                if project.project_manager == request.user:
                    return f(request, *args, **kwargs)
                else:
                    raise Http404
            else:
                raise Http404
        else:
            return redirect(reverse('login'))

    return check_authentication


# To check a logged in user is  member of that project of which he is viewing the story


def story_view_check(f):
    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            if Story.objects.filter(id=kwargs['pk']).exists():
                story = Story.objects.get(id=kwargs['pk'])
                if story.visibility:
                    project = story.project_title
                    temp = project.assigned_to.all()
                    if temp.filter(email=request.user.email):
                        return f(request, *args, **kwargs)
                    else:
                        raise Http404
                else:
                    raise Http404
            else:
                raise Http404
        else:
            return redirect(reverse('login'))

    return check_authentication


# View for signup


class SignupView(CreateView):
    form_class = form.SignupForm
    template_name = 'issue_models/myuser_form.html'

    # To login the new user and send the confirmation mail.

    def form_valid(self,form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        form.save()
        subject = 'Successful registration'
        message = ' You have been successfully registered in issue tracker'
        from_email = settings.EMAIL_HOST_USER
        to_mail = email
        send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        user = authenticate(email=email, password=password)
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('dashboard'))


# View for Login in to the dashboard


class LoginView(FormView):
    form_class = form.LoginForm
    template_name = "issue_models/login.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(reverse('dashboard'))


# View for logout


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse('homepage'))


# View of dashboard showing profile page link, Create project and various project in which user in involved.


class DashBoardView(ListView):
    template_name = "issue_models/dash.html"
    model = Project
    paginate_by = 5

    # To send the id in filter_code
    def get_context_data(self, **kwargs):
        context = super(DashBoardView, self).get_context_data(**kwargs)
        context['filter_code'] = self.request.GET.get('id')
        return context

    # To have different queryset for All Member Owner of project.
    def get_queryset(self):
        filter_id = self.request.GET.get('id')
        project = Project.objects.filter(assigned_to=self.request.user)
        if filter_id == '1':
            project = Project.objects.filter(assigned_to=self.request.user)
        if filter_id == '3':
            project = Project.objects.filter(project_manager=self.request.user)
        if filter_id == '2':
            temp = Project.objects.exclude(project_manager=self.request.user)
            project = temp.filter(assigned_to=self.request.user)
        return project


# To show the profile info. and profile update


class ProfileView(TemplateView):
    template_name = "issue_models/profile.html"


# View to update Profile


class ProfileUpdateView(FormView):
    template_name = "issue_models/profile_update.html"
    model = MyUser
    form_class = form.ProfileUpdateForm
    second_form_class = form.ChangePasswordForm
    success_url = reverse_lazy('profile')

    def get_form_class(self):
        if "form2" in self.request.POST:
            return self.second_form_class
        else:
            return self.form_class

    def get_form(self, form_class=None):
        form_class = self.get_form_class()
        if "form2" in self.request.POST:
            form_class=self.second_form_class(user=self.request.user, **self.get_form_kwargs())
        else:
            form_class = form.ProfileUpdateForm(instance=self.request.user, **self.get_form_kwargs())
        return form_class

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['form2'] = self.second_form_class(user=self.request.user)
        if "form2" in self.request.POST:
            context['form2'] = context['form']
            context['form'] = form.ProfileUpdateForm(instance=self.request.user)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        form.save()
        return super(ProfileUpdateView,self).form_valid(form)


# View to Create Project
class CreateProjectView(CreateView):
    template_name = "issue_models/createproject.html"
    form_class = form.CreateProjectForm
    success_url = reverse_lazy('dashboard')

    # To send request to the form
    def get_form_kwargs(self):
        kwargs = super(CreateProjectView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# View To see project details and story of a project
class ProjectView(DetailView):
    template_name = "issue_models/project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        story_all = Story.objects.filter(project_title=self.object.id)
        story_visible = story_all.filter(visibility=True).order_by('date')
        sch_story = story_visible.filter(scheduled='ys')
        unsch_story = story_visible.filter(scheduled='no')
        unstarted = sch_story.filter(status='unstrtd')
        started = sch_story.exclude(status='unstrtd')
        context['started'] = started
        context['unstarted'] = unstarted
        context['unsch_story'] = unsch_story
        return context


# View To update the project
class ProjectUpdateView(UpdateView):
    template_name = "issue_models/updateproject.html"
    model = Project
    context_object_name = 'project'
    form_class = form.UpdateProjectForm

    def get_success_url(self):
        project_id = self.kwargs['pk']
        return reverse_lazy('project', kwargs={'pk': project_id})

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['id'] = self.kwargs['pk']
        return kwargs


# View to add story to the project
class AddStoryView(FormView):

    form_class = formset_factory(AddStoryForm, formset=AddStoryFormSet, extra=0,min_num=1)
    template_name = "issue_models/addstory.html"

    def get_form_kwargs(self):
        kwargs = super(AddStoryView, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self,  **kwargs):
        context = super(AddStoryView, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        for f in form:
            obj = f.save(commit=False)
            obj.project_title = Project.objects.get(id=self.kwargs['pk'])
            obj.email = self.request.user
            obj.save()
        return super(AddStoryView, self).form_valid(form)

    def get_success_url(self):
        project_id = self.kwargs['pk']
        return reverse('project', kwargs={'pk': project_id})


# View to show story
class StoryView(DetailView):
    model = Story
    template_name = "issue_models/viewstory.html"


# view to update the story
class UpdateStoryView(UpdateView):
    model = Story
    template_name = "issue_models/story_update.html"
    form_class = form.UpdateStoryForm

    def get_form_kwargs(self):
        kwargs = super(UpdateStoryView, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        assigned = form.cleaned_data['assignee']
        result = Story.objects.filter(assignee=assigned).exists()
        if result == False:
            subject = self.object.story_title
            message = ' You have been assigned to story'
            from_email = settings.EMAIL_HOST_USER
            to_mail = self.object.assignee.email
            send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        return super(UpdateStoryView, self).form_valid(form)

    def get_success_url(self):
        project_id = self.get_object().project_title.id
        return reverse('project', kwargs={'pk': project_id})


# view to softly delete a story
class StoryDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        story = get_object_or_404(Story, pk=id)
        story.visibility = False
        story.save()
        project_id = story.project_title.id
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': project_id}))


class SearchStoryView(View):
    template_name = "issue_models/story_search.html"

    def dispatch(self, request, *args, **kwargs):
        search_text = self.request.GET.get('search_text')
        print len(search_text)
        items = search_text.split(',')
        x = [a for a in items if a]
        project_id = self.kwargs['pk']
        if ((len(search_text) != 0) and (search_text!=",") and (x)) :
            story = Story.objects.filter(reduce(operator.or_, (Q(story_title__icontains=item) & Q(visibility='ys') for item in x)))
            stories = story.filter(project_title_id = project_id)
            response = [{'story_title': story.story_title} for story in stories]
        else:
            response = [{'story_title': "Please enter search word"}]
        return HttpResponse(json.dumps(response), content_type="application/json")

class ProjectSettingView(DetailView):
    template_name = "issue_models/project_settings.html"
    model = Project

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            context =dict()
            initial_date = self.request.GET.get('initial_date')
            final_date = self.request.GET.get('final_date')

            context = self.story(context,initial_date,final_date)
            data = render_to_string('issue_models/story_table.html', context=context)
            if(self.request.GET.get('mail')):
                tasks.email.delay(data, self.request.user.email)
            return HttpResponse(data,content_type="html")
        return super(ProjectSettingView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        id = self.kwargs['pk']
        context = super(ProjectSettingView, self).get_context_data(**kwargs)
        initial = (Story.objects.filter(project_title=id)).order_by('date')
        if(initial):
            initial_date = initial[0].date
        else:
            initial_date=datetime.date.today()
        context = self.story(context, initial_date, datetime.date.today())

        result = render_to_string('issue_models/story_table.html', context=context)
        context['result'] = result
        context['init']=initial_date
        context['final']=datetime.date.today()
        return context
        # return self.render_to_response(context=context)

    def story(self, context,initial_date,final_date):
        id = self.kwargs['pk']
        project = Project.objects.get(id = id)
        story = (Story.objects.filter(project_title=id, visibility='ys', date__range=(initial_date,final_date))).order_by('assignee','status')
        assignee = project.assigned_to.all()
        list = []
        estimate = []
        i = 0
        for each in assignee:
            list.append([])
            estimate.append([])
            list[i].append(story.filter(assignee=each, status='finish').count())
            estimate[i].append(story.filter(assignee=each, status='finish').aggregate(Sum('estimate')))
            list[i].append(story.filter(assignee=each, status='strtd').count())
            estimate[i].append((story.filter(assignee=each, status='strtd')).aggregate(Sum('estimate')))
            list[i].append(story.filter(assignee=each, status='unstrtd').count())
            estimate[i].append((story.filter(assignee=each, status='unstrtd')).aggregate(Sum('estimate')))
            i = i+1
        unassigned_story = (Story.objects.filter(project_title=id, visibility='ys', assignee=None)).\
            order_by('assignee','status')
        no_unassigned = unassigned_story.count()
        no_estimate = unassigned_story.aggregate(Sum('estimate'))
        context['zipped_values'] = izip(assignee, list, estimate)
        context['unassigned_story'] = unassigned_story
        context['no_unassigned'] = no_unassigned
        context['no_estimate'] = no_estimate
        return context