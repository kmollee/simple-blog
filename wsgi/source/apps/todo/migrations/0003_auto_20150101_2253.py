# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_list_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='author',
            field=models.ForeignKey(default='', to=settings.AUTH_USER_MODEL, related_name='todo_list'),
            preserve_default=False,
        ),
    ]
