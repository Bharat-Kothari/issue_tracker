# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


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
                ('emailaddr', models.EmailField(help_text=b'Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, max_length=50, verbose_name=b'emailaddr', error_messages={b'unique': b'A emailaddr with that already exists.'})),
                ('first_name', models.CharField(max_length=30, verbose_name=b'first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name=b'last name', blank=True)),
                ('dob', models.DateField(null=True, verbose_name=b'date of bith')),
                ('photo', models.ImageField(upload_to=b'', blank=True)),
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
            name='new_project',
            fields=[
                ('projtitle', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=500)),
                ('emailadd', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='project_member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('emailadd', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('projtitle', models.ForeignKey(to='issue_models.new_project')),
            ],
        ),
        migrations.CreateModel(
            name='stories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('storytitle', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('estimate', models.IntegerField(verbose_name=b'in hours')),
                ('status', models.CharField(max_length=5, choices=[(b'strtd', b'started'), (b'finish', b'finished'), (b'deliv', b'delivered')])),
                ('scheduled', models.CharField(max_length=2, choices=[(b'ys', b'yes'), (b'no', b'no')])),
                ('visibilty', models.BooleanField(default=True)),
                ('assignee', models.ForeignKey(to='issue_models.project_member')),
                ('emailadd', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('projtitle', models.ForeignKey(to='issue_models.new_project')),
            ],
        ),
    ]
