# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlquery', '0002_auto_20170719_0224'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='cluster_db',
            field=models.CharField(default='', max_length=64, verbose_name='库名'),
        ),
    ]
