# -*- coding: UTF-8 -*-

from django.db import models

from common.aes_decryptor import Prpcrypt

# Create your models here.
# 各个线上主库地址。
class mysql_cluster_config(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_role = models.IntegerField('集群role', default=1)  # 1 master 0 slave -1 arbiter
    cluster_host = models.CharField('主从库地址JSON格式', max_length=100)
    cluster_port = models.IntegerField('集群端口', default=3306)
    cluster_user = models.CharField('登录集群的用户名', max_length=15)
    cluster_password = models.CharField('登录集群的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    cluster_status = models.IntegerField('集群状态', default=1)

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.cluster_password = pc.encrypt(self.cluster_password)
        super(mysql_cluster_config, self).save(*args, **kwargs)


class redis_cluster_config(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_role = models.IntegerField('集群role', default=1)  # 1 master 0 slave -1 arbiter
    cluster_host = models.CharField('主从库地址JSON格式', max_length=100)
    cluster_port = models.IntegerField('集群端口', default=3306)
    cluster_user = models.CharField('登录集群的用户名', max_length=15)
    cluster_password = models.CharField('登录集群的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    cluster_status = models.IntegerField('集群状态', default=1)

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.cluster_password = pc.encrypt(self.cluster_password)
        super(redis_cluster_config, self).save(*args, **kwargs)


class mongodb_cluster_config(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_role = models.IntegerField('集群role', default=1)  # 1 master 0 slave -1 arbiter
    cluster_host = models.CharField('主从库地址JSON格式', max_length=100)
    cluster_port = models.IntegerField('集群端口', default=3306)
    cluster_user = models.CharField('登录集群的用户名', max_length=15)
    cluster_password = models.CharField('登录集群的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    cluster_status = models.IntegerField('集群状态', default=1)

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.cluster_password = pc.encrypt(self.cluster_password)
        super(mongodb_cluster_config, self).save(*args, **kwargs)



# 集群类型
CLUSTER_ROLE = {
    1: '主库',
    0: '从库',
    -1: '仲裁',
}

# 集群状态
CLUSTER_STATUS = {
    0: '离线',
    1: '在线',
}