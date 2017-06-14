# -*- coding: UTF-8 -*-

from django.db import models

from common.aes_decryptor import Prpcrypt

# Create your models here.
# 各个线上主库地址。
class cluster_config(models.Model):
    cluster_type = models.IntegerField('集群类型', default=1)
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_hosts = models.CharField('主从库地址JSON格式', max_length=100)     # 主从库list通过json序列化后存入, 0位为主库地址
    cluster_port = models.IntegerField('集群端口', default=3306)
    cluster_user = models.CharField('登录集群的用户名', max_length=15)
    cluster_password = models.CharField('登录集群的密码', max_length=300)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    cluster_status = models.IntegerField('集群状态', default=1)

    def save(self, *args, **kwargs):
        pc = Prpcrypt()  # 初始化
        self.cluster_password = pc.encrypt(self.cluster_password)
        super(cluster_config, self).save(*args, **kwargs)

# 集群类型
CLUSTER_TYPE = {
    1: 'MySQL',
    2: 'Redis',
}

# 集群状态
CLUSTER_STATUS = {
    0: '离线',
    1: '在线',
}