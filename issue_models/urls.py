from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views


urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name="issue_models/home.html"), name='homepage'),
    url(r'^signup/$', views.loginCheck(views.SignupView.as_view()), name='signup'),
    url(r'^login/$', views.loginCheck(views.LoginView.as_view()), name='login'),
    url(r'^dashboard/$', views.logoutCheck(views.DashBoard.as_view()), name='dashboard'),
    url(r'^create/project/$',views.CreateProject.as_view(),name='create'),
    url(r'^dash/logout/$', views.logoutCheck(views.LogoutView.as_view()), name='logout'),
    url(r'^profile/$', views.logoutCheck(views.ProfileView.as_view()),name='profile'),
    url(r'^profile/update/$', views.logoutCheck(views.ProfileUpdate.as_view()), name='update_profile'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.projectMemberCheck(views.ProjectView.as_view()), name='project'),
    url(r'^projects/update/(?P<pk>[0-9 ]+)/$', views.projectUpdateCheck(views.ProjectUpdate.as_view()), name='updateproject'),
    url(r'^projects/story/add/(?P<pk>[0-9 ]+)/$', views.projectMemberCheck(views.AddStory.as_view()), name='addstory'),
    url(r'^projects/story/update/(?P<pk>[0-9 ]+)/$', views.storyViewCheck(views.UpdateStory.as_view()), name='updatestory'),
    url(r'^projects/story/view/(?P<pk>[0-9 ]+)/$', views.storyViewCheck(views.StoryView.as_view()), name='storyview'),
    url(r'^projects/story/delete/(?P<pk>[0-9 ]+)/$', views.storyViewCheck(views.StoryDelete.as_view()), name='storydelete'),
]

