# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0003_auto_20150715_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.ImageField(default=b'/home/josh/django-rampup/Issue_Track/media/images', upload_to=b'images', blank=True),
        ),
    ]
