# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('body', models.TextField(blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='todo_comment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('created_date', models.DateField(auto_now=True, auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('completed', models.BooleanField(default=None)),
                ('completed_date', models.DateField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('priority', models.PositiveIntegerField(max_length=3)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='todo_created_by')),
            ],
            options={
                'ordering': ['priority'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('slug', models.SlugField(editable=False, max_length=60)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Lists',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='list',
            unique_together=set([('slug',)]),
        ),
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.ForeignKey(to='todo.List'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(to='todo.Item'),
            preserve_default=True,
        ),
    ]
