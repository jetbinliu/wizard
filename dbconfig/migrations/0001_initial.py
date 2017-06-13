# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-12 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cluster_config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cluster_type', models.CharField(default='MySQL', max_length=10, verbose_name='集群类型')),
                ('cluster_name', models.CharField(max_length=50, verbose_name='集群名称')),
                ('cluster_hosts', models.CharField(max_length=100, verbose_name='主库地址')),
                ('cluster_port', models.IntegerField(default=3306, verbose_name='主库端口')),
                ('cluster_user', models.CharField(max_length=15, verbose_name='登录主库的用户名')),
                ('cluster_password', models.CharField(max_length=300, verbose_name='登录主库的密码')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
        ),
    ]