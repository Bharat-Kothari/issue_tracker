from django.views.generic import TemplateView
from django.conf.urls import url, include

from issue_tracker import views
from Issue_Track import decorators



story = [
    url(r'^add/(?P<pk>[0-9 ]+)/$', decorators.project_member_check(views.AddStoryView.as_view()), name='addstory'),
    url(r'^update/(?P<pk>[0-9 ]+)/$', decorators.story_view_check(views.UpdateStoryView.as_view()), name='updatestory'),
    url(r'^view/(?P<pk>[0-9 ]+)/$', decorators.story_view_check(views.StoryView.as_view()), name='storyview'),
    url(r'^delete/(?P<pk>[0-9 ]+)/$', decorators.story_view_check(views.StoryDeleteView.as_view()), name='storydelete'),
]


project =[
    url(r'^update/(?P<pk>[0-9 ]+)/$', decorators.project_update_check(views.ProjectUpdateView.as_view()), name='updateproject'),
    url(r'^story/',include(story)),
]

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="issue_tracker/home.html"), name='homepage'),
    url(r'^dashboard/$', decorators.logout_check(views.DashBoardView.as_view()), name='dashboard'),
    url(r'^create/project/$', decorators.logout_check(views.CreateProjectView.as_view()), name='create'),
    url(r'^project/(?P<pk>[0-9]+)/$', decorators.project_member_check(views.ProjectView.as_view()), name='project'),
    url(r'^projects/', include(project)),
    url(r'^search/story/(?P<pk>[0-9 ]+)/$', decorators.project_member_check(views.SearchStoryView.as_view()), name='searchstory'),
    url(r'^project/settings/(?P<pk>[0-9 ]+)/$', decorators.project_update_check(views.ProjectSettingView.as_view()), name='project_settings'),
    ]
