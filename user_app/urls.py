from django.views.generic import TemplateView
from django.conf.urls import url, include

from Issue_Track import decorators
from user_app import views


from django.conf.urls import  patterns
from tastypie.api import Api
from api import UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="user_app/home.html"), name='homepage'),
    url(r'^signup/$', decorators.login_check(views.SignupView.as_view()), name='signup'),
    url(r'^login/$', decorators.login_check(views.LoginView.as_view()), name='login'),
    url(r'^dash/logout/$', decorators.logout_check(views.LogoutView.as_view()), name='logout'),
    url(r'^profile/$', decorators.logout_check(views.ProfileView.as_view()), name='profile'),
    url(r'^profile/update/$', decorators.logout_check(views.ProfileUpdateView.as_view()), name='update_profile'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^', include("issue_tracker.urls")),

]