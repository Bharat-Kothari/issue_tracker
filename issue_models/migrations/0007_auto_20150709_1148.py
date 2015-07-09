# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0006_auto_20150709_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 11, 48, 3, 765464)),
        ),
    ]
