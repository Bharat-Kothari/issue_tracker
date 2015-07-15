# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0002_auto_20150714_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='scheduled',
            field=models.CharField(default=b'no', max_length=2, choices=[(b'ys', b'yes'), (b'no', b'no')]),
        ),
    ]
