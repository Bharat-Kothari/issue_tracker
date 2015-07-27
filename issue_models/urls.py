import django.contrib.auth.views
from django.views.generic import TemplateView
from django.conf.urls import url
from issue_models import views, form


urlpatterns = [
    url(r'^signup/$', views.login_check(views.SignupView.as_view()), name='signup'),
    url(r'^login/$', views.login_check(views.LoginView.as_view()), name='login'),
    url(r'^dashboard/$', views.logout_check(views.DashBoardView.as_view()), name='dashboard'),
    url(r'^create/project/$', views.logout_check(views.CreateProjectView.as_view()), name='create'),
    url(r'^dash/logout/$', views.logout_check(views.LogoutView.as_view()), name='logout'),
    url(r'^profile/$', views.logout_check(views.ProfileView.as_view()), name='profile'),
    url(r'^profile/update/$', views.logout_check(views.ProfileUpdateView.as_view()), name='update_profile'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.project_member_check(views.ProjectView.as_view()), name='project'),
    url(r'^projects/update/(?P<pk>[0-9 ]+)/$', views.project_update_check(views.ProjectUpdateView.as_view()), name='updateproject'),
    url(r'^projects/story/add/(?P<pk>[0-9 ]+)/$', views.project_member_check(views.AddStoryView.as_view()), name='addstory'),
    url(r'^projects/story/update/(?P<pk>[0-9 ]+)/$', views.story_view_check(views.UpdateStoryView.as_view()), name='updatestory'),
    url(r'^projects/story/view/(?P<pk>[0-9 ]+)/$', views.story_view_check(views.StoryView.as_view()), name='storyview'),
    url(r'^projects/story/delete/(?P<pk>[0-9 ]+)/$', views.story_view_check(views.StoryDeleteView.as_view()), name='storydelete'),
    url(r'^password_change/$', django.contrib.auth.views.password_change, {'template_name': 'issue_models/password_reset.html','post_change_redirect': 'update_profile', 'password_change_form': form.ChangePasswordForm }, name='changepassword'),
    url(r'^search/story/(?P<pk>[0-9 ]+)/$', views.SearchStoryView.as_view(), name='searchstory'),
    url(r'^project/settings/(?P<pk>[0-9 ]+)/$', views.ProjectSettingView.as_view(), name='project_settings'),
]

