# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue_models', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='Assigned_to',
            new_name='assigned_to',
        ),
    ]
