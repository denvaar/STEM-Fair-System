# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge_app', '0005_auto_20160216_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='award',
            name='number_of_winners',
            field=models.IntegerField(default=3),
        ),
    ]
