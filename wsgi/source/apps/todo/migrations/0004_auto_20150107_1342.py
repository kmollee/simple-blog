# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_auto_20150101_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-priority']},
        ),
        migrations.AlterField(
            model_name='item',
            name='completed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='priority',
            field=models.PositiveIntegerField(default=1, max_length=2, choices=[(0, 'LOW'), (1, 'MIDDLE'), (2, 'HIGH')]),
            preserve_default=True,
        ),
    ]
