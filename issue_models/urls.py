from django.conf.urls import url

from . import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="issue_models/home.html")),
    url(r'^signup/$', views.SignupCreate.as_view(),name='signup'),
    url(r'^success/$', TemplateView.as_view(template_name="issue_models/successful.html")),
    url(r'^login/$', 'django.contrib.auth.views.login' ,{'template_name': 'login.html'}, name='login'),
    url(r'^dash/$', TemplateView.as_view(template_name="issue_models/dash.html"), name='dashboard'),
    url(r'^login1/$', views.Login.as_view()),
    url(r'^dash/logout/$', views.logout_view.as_view(), name='logout'),
    url('^profile/$', views.ProfileView.as_view(),name='profile'),
    url('^profile/update/$', views.ProfileUpdate.as_view(), name='update_profile'),
]

