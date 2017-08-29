# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-27 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbconfig', '0017_mysql_cluster_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='auto_increment',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='avg_row_length',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='data_free',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='data_length',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='index_length',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='mysql_cluster_metadata',
            name='max_data_length',
            field=models.BigIntegerField(),
        ),
    ]
