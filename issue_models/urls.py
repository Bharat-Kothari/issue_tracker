from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views


urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="issue_models/home.html")),
    url(r'^signup/$', views.SignupCreate.as_view(),name='signup'),
    url(r'^dash/$', views.Dash.as_view(), name='dashboard'),
    url(r'^login/$', views.login_check(views.Login.as_view()), name='login1'),
    url(r'^create/$',views.CreateProject.as_view(),name='create'),
    url(r'^dash/logout/$', views.logout_view.as_view(), name='logout'),
    url(r'^profile/$', views.ProfileView.as_view(),name='profile'),
    url(r'^profile/update/$', views.ProfileUpdate.as_view(), name='update_profile'),
    url(r'^project/(?P<pk>[a-z ]+)/$', views.ProjectView.as_view(), name='project'),
    url(r'^projects/update/(?P<pk>[a-z ]+)/$', views.ProjectUpdate.as_view(), name='updateproject'),
    url(r'^projects/addstory/(?P<pk>[a-z ]+)/$', views.AddStory.as_view(), name='addstory'),
    url(r'^projects/storyupdate/(?P<pk>[0-9 ]+)/$', views.UpdateStory.as_view(), name='updatestory'),
    url(r'^projects/storyview/(?P<pk>[0-9 ]+)/$', views.StoryView.as_view(), name='storyview'),
    url(r'^projects/storydelete/(?P<pk>[0-9 ]+)/$', views.StoryDelete.as_view(), name='storydelete'),
]

