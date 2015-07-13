# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(help_text=b'Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=50, verbose_name=b'email', error_messages={b'unique': b'A email with that already exists.'})),
                ('first_name', models.CharField(max_length=30, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name=b'last name', blank=True)),
                ('dob', models.DateField(null=True, verbose_name=b'date of birth')),
                ('photo', models.ImageField(upload_to=b'images', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text=b'Designates whether the user can log into this admin site.', verbose_name=b'staff status')),
                ('is_active', models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name=b'active')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500)),
                ('Assigned_to', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project_manager', models.ForeignKey(related_name='Manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('story_title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('estimate', models.IntegerField(verbose_name=b'in hours')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('status', models.CharField(default=b'unstrtd', max_length=7, choices=[(b'unstrtd', b'notstarted'), (b'strtd', b'started'), (b'finish', b'finished'), (b'deliv', b'delivered')])),
                ('scheduled', models.CharField(max_length=2, choices=[(b'ys', b'yes'), (b'no', b'no')])),
                ('visibility', models.BooleanField(default=True)),
                ('assignee', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('email', models.ForeignKey(related_name='Story_Creator', to=settings.AUTH_USER_MODEL)),
                ('project_title', models.ForeignKey(to='issue_models.Project')),
            ],
        ),
    ]
