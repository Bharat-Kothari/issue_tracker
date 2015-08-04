from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.mail import send_mail

from Issue_Track import settings
from user_app.models import MyUser
from user_app import form


class SignupView(CreateView):
    """
    View for signup
    """
    form_class = form.SignupForm
    template_name = 'user_app/signup_form.html'

    # To login the new user and send the confirmation mail.

    def form_valid(self, form):
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
    template_name = "user_app/login.html"

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data["password"]
        email_check = MyUser.objects.get(email__iexact=email)
        user = authenticate(email=email_check.email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(reverse('dashboard'))


# View for logout


class LogoutView(View):
    def get(self, request):
        logout(self.request)
        return redirect(reverse('homepage'))


class ProfileView(TemplateView):
    """
    To show the profile information.
    Profile update Link
    """

    template_name = "user_app/profile/profile.html"


class ProfileUpdateView(FormView):
    """
    View to update Profile
    Update Password
    """
    template_name = "user_app/profile/profile_update.html"
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
        if "form2" in self.request.POST:
            form_class = self.second_form_class(user=self.request.user, **self.get_form_kwargs())
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
        return super(ProfileUpdateView, self).form_valid(form)
