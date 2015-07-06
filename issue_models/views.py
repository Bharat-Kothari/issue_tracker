from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView
from issue_models.models import MyUser, new_project
from issue_models import form
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


def login_check(f):
    def check_authentication(request, *args):
        if request.user.is_authenticated():
            print 'bharat'
            return redirect('/home/dash/')
        else:
            return f(request)
    return check_authentication


class SignupCreate(CreateView):
    form_class = form.SignupForm
    model = MyUser
    template_name = 'issue_models/myuser_form.html'
    def form_valid(self, form):
        emailaddr = self.request.POST['emailaddr']
        password = self.request.POST['password']
        form.save()
        user = authenticate(emailaddr=emailaddr, password=password)
        login(self.request,user)
        return HttpResponseRedirect('/home/dash/')


class Login(FormView):

    form_class = form.LoginForm
    template_name = "issue_models/login1.html"
    def form_valid(self, form):
        emailaddr = self.request.POST['emailaddr']
        password = self.request.POST['password']
        user = authenticate(emailaddr=emailaddr, password=password)

        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(self.request,user)
                print("User is valid, active and authenticated")
                return HttpResponseRedirect('/home/dash/')
            else:
                print("The password is valid, but the account has been disabled!")
                return HttpResponse("invalid")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
        return HttpResponseRedirect('/home/login1/')

class logout_view(View):
    print 'working1'
    def get(self, request):
        print 'working2'
        logout(self.request)
        print 'working3'
        return redirect('/home/login/')

class Dash(TemplateView):
    template_name="issue_models/dash.html"
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Dash, self).dispatch(request, *args, **kwargs)

class ProfileView(TemplateView):

    template_name = "issue_models/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request,*args, **kwargs)

class ProfileUpdate(UpdateView):
    template_name = "issue_models/profile_update.html"
    model = MyUser
    form_class = form.ProfileUpdateForm
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileUpdate, self).dispatch(request,*args, **kwargs)

    success_url = reverse_lazy('profile')
    def get_object(self, queryset=None):
        return self.request.user


class CreateProject(CreateView):
    template_name = "issue_models/createproject.html"
    model = new_project
    form_class = form.CreateProjectForm

    def get_form_kwargs(self):
        kwargs = super(CreateProject, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
