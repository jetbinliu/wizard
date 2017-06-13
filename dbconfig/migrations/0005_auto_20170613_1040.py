# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconfig', '0004_auto_20170613_1039'),
    ]

    operations = [
        migrations.DeleteModel(
            name='cluster_type',
        ),
        migrations.AlterField(
            model_name='cluster_config',
            name='cluster_type',
            field=models.CharField(default='MySQL', max_length=10, verbose_name='集群类型'),
        ),
    ]
