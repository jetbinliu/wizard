# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 13:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sqlquery', '0005_auto_20170721_2109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workflow',
            name='finish_time',
        ),
    ]
