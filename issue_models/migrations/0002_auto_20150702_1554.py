# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=models.ImageField(upload_to=b'/images', blank=True),
        ),
    ]
