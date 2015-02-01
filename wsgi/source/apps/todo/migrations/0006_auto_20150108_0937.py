# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20150108_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='completed_date',
        ),
        migrations.RemoveField(
            model_name='item',
            name='due_date',
        ),
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
