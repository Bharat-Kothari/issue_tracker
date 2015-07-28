from __future__ import absolute_import
import os
from Issue_Track import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Issue_Track.settings')
app = Celery('Issue_Track')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)