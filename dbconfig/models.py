# -*- coding: UTF-8 -*-

from django.db import models

from common.aes_decryptor import Prpcrypt

# Create your models here.
# 各个线上实例地址。
class mysql_cluster_config(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_role = models.IntegerField('集群role', default=1)  # 1 master 0 slave -1 arbiter
    cluster_host = models.CharField('实例地址', max_length=100)
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
    cluster_host = models.CharField('实例地址', max_length=100)
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
    cluster_host = models.CharField('实例地址', max_length=100)
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


# 元数据
class mysql_cluster_metadata(models.Model):
    cluster_name = models.CharField('集群名称', max_length=50)  # 产品线
    cluster_port = models.IntegerField('集群端口', default=3306)
    table_schema = models.CharField(max_length=64, default='')
    table_name = models.CharField(max_length=64, default='')
    table_type = models.CharField(max_length=64, default='')
    engine = models.CharField(max_length=64, default='')
    row_format = models.CharField(max_length=20, default='')
    table_rows = models.BigIntegerField(default=0)
    avg_row_length = models.BigIntegerField(default=0)
    data_length = models.BigIntegerField(default=0)
    max_data_length = models.BigIntegerField(default=0)
    index_length = models.BigIntegerField(default=0)
    data_free = models.BigIntegerField(default=0)
    auto_increment = models.BigIntegerField(default=0)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    table_collation = models.CharField(max_length=32, default='')
    create_statement = models.TextField(default='')
    create_options = models.CharField(max_length=255, default='')
    table_comment = models.CharField(max_length=2048, default='')
