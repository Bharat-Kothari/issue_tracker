from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.static import serve
from Issue_Track import settings
import issue_models

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
#admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include('issue_models.urls')),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': getattr(settings, "MEDIA_ROOT"),}),

)
