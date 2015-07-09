# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0005_auto_20150709_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 9, 11, 41, 7, 487516)),
        ),
    ]
