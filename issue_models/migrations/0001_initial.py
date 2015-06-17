# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('emailadd', models.EmailField(max_length=75, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=30)),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
            ],
        ),
    ]
