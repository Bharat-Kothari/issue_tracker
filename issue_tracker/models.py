from datetime import datetime

from django.db import models
from user_app.models import MyUser


# Model for project
class Project(models.Model):

    project_manager = models.ForeignKey(MyUser, related_name='Manager')
    project_title = models.CharField(max_length=30)
    description = models.CharField(max_length=500, blank=True)
    assigned_to = models.ManyToManyField(MyUser, blank=True, null=True)

    def __unicode__(self):
        return self.project_title


# model for story of projects
class Story(models.Model):

    project_title = models.ForeignKey(Project)
    email = models.ForeignKey(MyUser, related_name='Story_Creator')
    story_title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    assignee = models.ForeignKey(MyUser, blank=True, null=True)
    estimate = models.PositiveIntegerField(default=0)
    date = models.DateField(default=datetime.now)
    unstrtd = 'unstrtd'
    strtd = 'strtd'
    finish = 'finish'
    deliv = 'deliv'
    status_choice = (
        (unstrtd, 'notstarted'),
        (strtd, 'started'),
        (finish, 'finished'),
        (deliv, 'delivered')
    )
    status = models.CharField(max_length=7, choices=status_choice, default=unstrtd)
    ys = 'ys'
    no = 'no'
    scheduled_choice = (
        (ys, 'yes'),
        (no, 'no')
    )
    scheduled = models.CharField(max_length=2, choices=scheduled_choice, default=no)
    visibility = models.BooleanField(default=True)

    def __unicode__(self):
        return self.story_title