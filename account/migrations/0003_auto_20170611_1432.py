# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170611_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.IntegerField(blank=True, default=5),
        ),
    ]
