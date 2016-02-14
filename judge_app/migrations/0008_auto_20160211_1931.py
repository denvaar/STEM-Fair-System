# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-11 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_app', '0007_auto_20160211_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='award',
            name='project',
        ),
        migrations.AddField(
            model_name='award',
            name='projects',
            field=models.ManyToManyField(blank=True, to='judge_app.Project'),
        ),
    ]
