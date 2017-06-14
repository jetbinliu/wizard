# -*- coding: UTF-8 -*-

import json

from django.db.models import Q

from .models import cluster_config as Cluster
from common.aes_decryptor import Prpcrypt
import pymysql as mdb



def getClusterDbs(host, port, user, passwd):
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

def getClusterInfo(flag='online'):

    dictAllClusterDetail = {}
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
        cluster_id = cluster.id
        cluster_name = cluster.cluster_name
        cluster_host = json.loads(cluster.cluster_hosts)[0]
        cluster_port = cluster.cluster_port
        cluster_user = cluster.cluster_user
        cluster_password = cluster.cluster_password
        cluster_create_time = cluster.create_time
        cluster_status = cluster.cluster_status

        pc = Prpcrypt()  # 初始化
        cluster_password = pc.decrypt(cluster_password)
        if cluster_status :
            try:
                dbs = getClusterDbs(cluster_host, cluster_port, cluster_user, cluster_password)
            except Exception as e:
                dbs = [e]
        else:
            dbs = []
        dictAllClusterDetail[cluster_name] = [cluster_id, cluster_host, cluster_port, dbs,
                                              cluster_status, cluster_create_time]
    return dictAllClusterDetail


def setClusterStatusByPort(port,stat):
    try:
        Cluster.objects.filter(cluster_port=int(port)).update(cluster_status=int(stat))
        return {'status': 0}
    except Exception as e:
        print(e)
        return {'status': 1}