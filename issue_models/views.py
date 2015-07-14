from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from Issue_Track import settings
from issue_models.models import MyUser, Project, Story
from issue_models import form

# to check user is already logged in.


def loginCheck(f):

    def check_authentication(request, *args):
        if request.user.is_authenticated():
            return redirect(reverse_lazy('dashboard'))
        else:
            return f(request)
    return check_authentication

# to check user has logged in.


def logoutCheck(f):

    def check_authentication(request, *args, **kwargs):
        if request.user.is_authenticated():
            return f(request,*args, **kwargs)
        else:
            return redirect(reverse('login'))
    return check_authentication

def projectMemberCheck(f):
    def check_authentication(request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['pk'])
        temp = project.assigned_to.all()
        if request.user.is_authenticated():
            if temp.filter(email = request.user.email):
                return f(request,*args, **kwargs)
            else:
                raise Http404
    return check_authentication

def projectUpdateCheck(f):
    def check_authentication(request, *args, **kwargs):
        project = Project.objects.get(id=kwargs['pk'])
        print project
        if request.user.is_authenticated():
            if project.project_manager==request.user:
                return f(request,*args, **kwargs)
            else:
                raise Http404
    return check_authentication

def storyViewCheck(f):
    def check_authentication(request, *args, **kwargs):
        story = Story.objects.get(id=kwargs['pk'])
        print story
        if story.visibility:
            project= story.project_title
            print project
            temp = project.assigned_to.all()
            print temp
            print request.user.email
            if request.user.is_authenticated():
                if temp.filter(email = request.user.email):
                    return f(request,*args, **kwargs)
                else:
                    raise Http404
        else:
            raise Http404
    return check_authentication


class SignupView(CreateView):
    form_class = form.SignupForm
    template_name = 'issue_models/myuser_form.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        print password
        form.save()
        subject = 'Successful registration'
        message = ' You have been successfully registered in issue tracker'
        from_email = settings.EMAIL_HOST_USER
        to_mail = email
        send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        user = authenticate(email=email, password=password)
        print user
        login(self.request, user)
        return HttpResponseRedirect(reverse_lazy('dashboard'))


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
                print("User is valid, active and authenticated")
                return HttpResponseRedirect(reverse_lazy('dashboard'))
            else:
                print("The password is valid, but the account has been disabled!")
                return HttpResponse("invalid")
        else:
            print("The username and password were incorrect123.")
        return HttpResponseRedirect(reverse_lazy('login'))


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse('homepage'))


class DashBoard(ListView):
    template_name = "issue_models/dash.html"
    model = Project
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context=super(DashBoard, self).get_context_data(**kwargs)
        context['filter_code']= self.request.GET.get('id')
        return context

    def get_queryset(self):
        filter_id=self.request.GET.get('id')
        if filter_id == '1':
            return Project.objects.filter(assigned_to=self.request.user)
        if filter_id == '3':
            return Project.objects.filter(project_manager=self.request.user)
        if filter_id == '2':
            temp = Project.objects.exclude(project_manager=self.request.user)
            member = temp.filter(assigned_to=self.request.user)
            return member
        return Project.objects.filter(assigned_to=self.request.user)


class ProfileView(TemplateView):

    template_name = "issue_models/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)


class ProfileUpdate(UpdateView):
    template_name = "issue_models/profile_update.html"
    model = MyUser
    form_class = form.ProfileUpdateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdate, self).dispatch(request, *args, **kwargs)
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user


class CreateProject(CreateView):
    template_name = "issue_models/createproject.html"
    form_class = form.CreateProjectForm
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super(CreateProject, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateProject, self).dispatch(request, *args, **kwargs)


class ProjectView(DetailView):

    template_name = "issue_models/project.html"
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectView, self).get_context_data(**kwargs)
        story_all = Story.objects.filter(project_title=self.object.id)
        print "number of story_all :"
        print story_all.count()
        story_visible = story_all.filter(visibility=True).order_by('date')
        sch_story = story_visible.filter(scheduled='ys')
        unsch_story = story_visible.filter(scheduled='no')
        unstarted = sch_story.filter(status='unstrtd')
        started = sch_story.exclude(status='unstrtd')
        context['started'] = started
        context['unstarted'] = unstarted
        context['unsch_story'] = unsch_story
        return context


class ProjectUpdate(UpdateView):
    template_name = "issue_models/updateproject.html"
    model = Project
    form_class = form.UpdateProjectForm

    def get_form_kwargs(self):
        kwargs = super(ProjectUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['id'] = self.kwargs['pk']
        return kwargs
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context=super(ProjectUpdate, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

class AddStory(CreateView):
    model = Story
    form_class = form.AddStoryForm
    template_name = "issue_models/addstory.html"

    def get_form_kwargs(self):
        kwargs = super(AddStory, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context=super(AddStory, self).get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        subject = form.cleaned_data['story_title']
        message = ' You have been assigned to story'
        from_email = settings.EMAIL_HOST_USER
        assignee = form.cleaned_data['assignee']
        to_mail = assignee.email
        send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        return super(AddStory,self).form_valid(form)

    def get_success_url(self):
        project_id = self.kwargs['pk']
        print project_id
        return reverse('project', kwargs={'pk': project_id})


class StoryView(DetailView):
    model = Story
    template_name = "issue_models/viewstory.html"


class UpdateStory(UpdateView):
    model = Story
    template_name = "issue_models/story_update.html"
    form_class = form.UpdateStoryForm

    def get_form_kwargs(self):
        kwargs = super(UpdateStory, self).get_form_kwargs()
        kwargs['id'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        assigned = form.cleaned_data['assignee']
        result = Story.objects.filter(assignee=assigned).exists()
        if result == False:
            subject = self.object.story_title
            print subject
            message = ' You have been assigned to story'
            from_email = settings.EMAIL_HOST_USER
            to_mail = self.object.assignee.email
            print to_mail
            send_mail(subject, message, from_email, [to_mail], fail_silently=True)
        return super(UpdateStory, self).form_valid(form)

    def get_success_url(self):
        project_id = self.get_object().project_title.id
        print project_id
        return reverse('project', kwargs={'pk': project_id})


class StoryDelete(View):

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        story = get_object_or_404(Story, pk=id)
        story.visibility = False
        story.save()
        project_id = story.project_title.id
        return HttpResponseRedirect(reverse_lazy('project', kwargs={'pk': project_id}))