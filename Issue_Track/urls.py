from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.views.static import serve
from Issue_Track import settings

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
#admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name="user_app/home.html")),
    url(r'^home/', include('user_app.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': getattr(settings, "MEDIA_ROOT"),}),

)
