# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0002_auto_20150708_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='status',
            field=models.CharField(default=b'unstrtd', max_length=7, choices=[(b'unstrtd', b'notstarted'), (b'strtd', b'started'), (b'finish', b'finished'), (b'deliv', b'delivered')]),
        ),
    ]
