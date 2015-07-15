# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0005_auto_20150715_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.ImageField(default=b'images/Facebook-Blank-Photo1.jpg', upload_to=b'images', blank=True),
        ),
    ]
