from django.shortcuts import HttpResponse

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View


# from django.shortcuts import render
# from django.http import HttpResponseRedirect
#
# from . import form
#
# def login_view(request):
#     log_form = form.LoginInfoForm(request.POST)
#
#     render(log_form)
#
# """
# def get_emailaddr(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = LoginInfoForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')


# from django.http import HttpResponse
# from django.views.generic import View
# import models
# class signup(View):
#     def get(self, request, pk):
#         person = models.MyUser.objects.get(pk=pk)
#         return render(
#             'people/hello.html',
#             {'person': person}
#         )


from django.views.generic.edit import CreateView, BaseCreateView
from issue_models.models import MyUser
from django.contrib.auth.hashers import make_password
from issue_models import form
class SignupCreate(CreateView):
    form_class = form.SignupForm
    model = MyUser
    template_name = 'issue_models/myuser_form.html'
    # fields = ['emailaddr', 'password', 'first_name', 'last_name', 'dob']
    # make_password('password')
    success_url = '/signup/success/'



# class Successful(View):
#     template_name = 'issue_models/successful.html'
#
# class Home(View):
#     template_name = 'issue_models/home.html'



from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View



from issue_models import form

class LoginView(View):

    form_class = form.LoginForm
    model = MyUser
    #fields = ['emailaddr', 'password']
    initial = {'key': 'value'}
    template_name = 'issue_models/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            return HttpResponseRedirect('/success/')

        return render(request, self.template_name, {'form': form})

