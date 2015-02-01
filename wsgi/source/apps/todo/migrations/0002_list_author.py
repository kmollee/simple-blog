# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='author',
            field=models.ForeignKey(blank=True, related_name='todo_list', null=True, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
    ]
