# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Headline', max_length=100)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ('-submitted_on',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='Headline', max_length=100)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
                ('submitter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id', 'submitted_on'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(unique=True, verbose_name='Title', max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='entry',
            name='tag',
            field=models.ManyToManyField(blank=True, to='blog.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='entry',
            field=models.ForeignKey(blank=True, default=None, to='blog.Entry'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='submitter',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
