# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0007_auto_20150709_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
