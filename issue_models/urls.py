from django.conf.urls import url

from . import views
from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views

urlpatterns = [
    url(r'^$', views.SignupCreate.as_view()),
    # url(r'^success/', views.Successful.as_view())
    url(r'^success/', TemplateView.as_view(template_name="issue_models/successful.html"))
]

