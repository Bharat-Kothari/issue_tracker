from django.shortcuts import HttpResponse

# Create your views here.
from django.http import HttpResponse
from django.views.generic import View


from django.views.generic.edit import UpdateView
from issue_models.form import LoginInfoForm

class LoginInfoView(UpdateView): # FormView
    form_class = LoginInfoForm
    #template = 'issue_models/basic.html'