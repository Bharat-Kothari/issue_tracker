from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail
from Issue_Track import settings
from Issue_Track.celery import app


@app.task
def email(message,to):
    print 'email'
    from_email = settings.EMAIL_HOST_USER
    send_mail("report1", "", from_email, [to], fail_silently=True, html_message=message)