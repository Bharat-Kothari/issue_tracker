from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.GreetingView.as_view()),
]
