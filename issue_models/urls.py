from django.conf.urls import url

from . import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="issue_models/home.html")),

    url(r'^signup/', views.SignupCreate.as_view()),
    #url(r'^login', views.LoginView.as_view()),
    url(r'^success/', TemplateView.as_view(template_name="issue_models/successful.html")),
    # url(r'^login/', auth_views.login),
    url(r'^login/$', 'django.contrib.auth.views.login' ,{'template_name': 'login.html'}, name='login'),
    url(r'^dash/', TemplateView.as_view(template_name="issue_models/dash.html")),
    url(r'^profile/', views.Profile.as_view() ),
]

