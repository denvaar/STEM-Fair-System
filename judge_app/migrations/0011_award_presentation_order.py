# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_app', '0010_auto_20160222_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='award',
            name='presentation_order',
            field=models.PositiveIntegerField(default=33),
        ),
    ]
