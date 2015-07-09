# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0003_auto_20150708_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='stories',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 11, 21, 19, 193613)),
        ),
    ]
