from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView
from issue_models.models import MyUser
from issue_models import form
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect


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
        return redirect('/home/login1/')


class ProfileView(TemplateView):

    template_name = "issue_models/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['myuser'] = self.request.user
        return context

class ProfileUpdate(UpdateView):
    template_name = "issue_models/profile_update.html"
    model = MyUser
    form_class = form.ProfileUpdateForm

    success_url = reverse_lazy('profile')
    def get_object(self, queryset=None):
        return self.request.user