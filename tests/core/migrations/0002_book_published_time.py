# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-05 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='published_time',
            field=models.TimeField(blank=True, null=True, verbose_name='Time published'),
        ),
    ]
