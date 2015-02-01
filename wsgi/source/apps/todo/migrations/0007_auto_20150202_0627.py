# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_auto_20150108_0937'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['completed', '-priority']},
        ),
    ]
