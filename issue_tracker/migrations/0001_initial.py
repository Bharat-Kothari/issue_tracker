# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500, blank=True)),
                ('assigned_to', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
                ('project_manager', models.ForeignKey(related_name='Manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('story_title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('estimate', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(default=b'unstrtd', max_length=7, choices=[(b'unstrtd', b'notstarted'), (b'strtd', b'started'), (b'finish', b'finished'), (b'deliv', b'delivered')])),
                ('scheduled', models.CharField(default=b'no', max_length=2, choices=[(b'ys', b'yes'), (b'no', b'no')])),
                ('visibility', models.BooleanField(default=True)),
                ('assignee', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('email', models.ForeignKey(related_name='Story_Creator', to=settings.AUTH_USER_MODEL)),
                ('project_title', models.ForeignKey(to='issue_tracker.Project')),
            ],
        ),
    ]
