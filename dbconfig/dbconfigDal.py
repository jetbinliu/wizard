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

def getAllMySQLClusterInfo(flag='online'):

    # 查询在线集群信息
    if flag == 'online':
        clusters = Cluster.objects.filter(Q(cluster_type=1) and Q(cluster_status=1))
    # 查询在线集群信息
    elif flag == 'offline':
        clusters = Cluster.objects.filter(Q(cluster_type=1) and Q(cluster_status=0))
    # 查询全部集群信息
    elif flag == 'all':
        clusters = Cluster.objects.filter(cluster_type=1)
    else:
        return None
    for cluster in clusters:
        cluster.cluster_password = prpCryptor.decrypt(cluster.cluster_password)
    return clusters


# 根据集群名获取主库连接字符串，并封装成一个dict
def getMasterConnStr(clusterName):
    listMasters = Cluster.objects.filter(cluster_name=clusterName)

    masterHost = json.loads(listMasters[0].cluster_hosts)[0]
    masterPort = listMasters[0].cluster_port
    masterUser = listMasters[0].cluster_user
    masterPassword = prpCryptor.decrypt(listMasters[0].cluster_password)
    dictConn = {'masterHost': masterHost, 'masterPort': masterPort, 'masterUser': masterUser,
                'masterPassword': masterPassword}
    return dictConn


def setClusterStatusByPort(cluster_type,port,stat):
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
        _dao.objects.filter(cluster_port=int(port)).update(cluster_status=int(stat))
        return {'status': 0}
    except Exception as e:
        print(e)
        return {'status': 1}