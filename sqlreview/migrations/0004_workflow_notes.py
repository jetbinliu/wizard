# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqlreview', '0003_delete_cluster_config'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='notes',
            field=models.CharField(default='', max_length=50, verbose_name='备注 JSON格式'),
        ),
    ]
