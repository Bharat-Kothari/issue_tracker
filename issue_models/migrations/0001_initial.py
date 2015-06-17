# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='new_project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projtitle', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='projects_member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='stories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('storytitle', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('assignee', models.CharField(max_length=50)),
                ('estimate', models.IntegerField(verbose_name=b'in hours')),
                ('status', models.CharField(max_length=5, choices=[(b'strtd', b'started'), (b'finsh', b'finished'), (b'deliv', b'delivered')])),
                ('scheduled', models.CharField(max_length=2, choices=[(b'ys', b'yes'), (b'no', b'no')])),
                ('visibilty', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('emailadd', models.EmailField(max_length=75, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='stories',
            name='emailadd',
            field=models.ForeignKey(to='issue_models.user_table'),
        ),
        migrations.AddField(
            model_name='stories',
            name='projtitle',
            field=models.ForeignKey(to='issue_models.new_project'),
        ),
        migrations.AddField(
            model_name='projects_member',
            name='emailadd',
            field=models.ForeignKey(to='issue_models.user_table'),
        ),
        migrations.AddField(
            model_name='projects_member',
            name='projtitle',
            field=models.ForeignKey(to='issue_models.new_project'),
        ),
        migrations.AddField(
            model_name='new_project',
            name='emailadd',
            field=models.ForeignKey(to='issue_models.user_table'),
        ),
    ]
