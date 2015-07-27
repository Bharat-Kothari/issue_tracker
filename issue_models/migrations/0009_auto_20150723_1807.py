# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0008_auto_20150715_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='estimate',
            field=models.PositiveIntegerField(),
        ),
    ]
