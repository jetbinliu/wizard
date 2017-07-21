# -*- coding: UTF-8 -*-

import json

from django.db.models import Q

from .models import mysql_cluster_config, redis_cluster_config, mongodb_cluster_config
from common.aes_decryptor import Prpcrypt
import pymysql as mdb

prpCryptor = Prpcrypt()  # 初始化

def getMySQLClusterDbs(host, port, user, passwd):
    dbs = []
    try:
        # Connect to the cluster database
        connection = mdb.connect(host=host,
                                 port=port,
                                 user=user,
                                 passwd=passwd,
                                 db='information_schema',
                                 charset='utf8mb4',
                                 cursorclass=mdb.cursors.DictCursor)

        # with connection.cursor() as cursor:
        cursor = connection.cursor()
        sql = "select schema_name from schemata where schema_name not in (" \
              "'mysql','sys','information_schema','performance_schema')"
        cursor.execute(sql)
        results = cursor.fetchall()
        dbs = [result['schema_name'] for result in results]
    except mdb.Warning as w:
        print(str(w))
    except mdb.Error as e:
        print(str(e))
    finally:
        connection.close()
    return dbs

def getAllMySQLInfo(cluster_role=1, flag='online'):

    # 查询在线集群信息
    if flag == 'online':
        clusters = mysql_cluster_config.objects.filter(Q(cluster_role=cluster_role) & Q(cluster_status=1))
    # 查询在线集群信息
    elif flag == 'offline':
        clusters = mysql_cluster_config.objects.filter(Q(cluster_role=cluster_role) & Q(cluster_status=0))
    # 查询全部集群信息
    elif flag == 'all':
        clusters = mysql_cluster_config.objects.filter(cluster_role=cluster_role)
    else:
        return None
    for cluster in clusters:
        cluster.cluster_password = prpCryptor.decrypt(cluster.cluster_password)
    return clusters


# 根据集群名获取主库连接字符串，并封装成一个dict
def getMasterConnStr(clusterName):
    listMasters = mysql_cluster_config.objects.filter(Q(cluster_name=clusterName) & Q(cluster_role=1))
    if len(listMasters) != 1:
        print("Error: 集群主库配置返回为0")
        return None
    Host = listMasters[0].cluster_host
    Port = listMasters[0].cluster_port
    User = listMasters[0].cluster_user
    Password = prpCryptor.decrypt(listMasters[0].cluster_password)
    dictConn = {'Host': Host, 'Port': Port, 'User': User,
                'Password': Password}
    return dictConn


# 根据集群名获取从库连接字符串，并封装成一个dict
def getSlaveConnStr(clusterName):
    listSlaves = mysql_cluster_config.objects.filter(Q(cluster_name=clusterName) & Q(cluster_role=0) & Q(cluster_status=1))
    if len(listSlaves) < 1:
        print("Error: 集群从库配置返回为0")
        return None
    Host = listSlaves[-1].cluster_host
    Port = listSlaves[-1].cluster_port
    User = listSlaves[-1].cluster_user
    Password = prpCryptor.decrypt(listMasters[0].cluster_password)
    dictConn = {'Host': Host, 'Port': Port, 'User': User,
                'Password': Password}
    return dictConn


def setClusterStatusByHostPort(cluster_type,host,port,stat):
    _cluster_type = cluster_type.lower()
    if _cluster_type == 'mysql':
        _dao = mysql_cluster_config
    elif _cluster_type == 'redis':
        _dao = redis_cluster_config
    elif _cluster_type == 'mongodb':
        _dao = mongodb_cluster_config
    else:
        return HttpResponse(status=403)

    try:
        _dao.objects.filter(Q(cluster_host=host) & Q(cluster_port=int(port))).update(cluster_status=int(stat))
        return {'status': 0}
    except Exception as e:
        print(e)
        return {'status': 1}