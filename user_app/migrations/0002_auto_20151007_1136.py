# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='dob',
            field=models.DateField(help_text=b'(yyyy/mm/dd)', null=True, verbose_name=b'date of birth'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(help_text=b'Letters, digits and @/./+/-/_ only.', unique=True, max_length=50, error_messages={b'unique': b'A email with that already exists.'}),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text=b'Designates whether this user should be treated as active.Un-select this instead of deleting accounts.', verbose_name=b'active'),
        ),
    ]
