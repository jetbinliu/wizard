# -*- coding: UTF-8 -*-

from django.db.models import Q

from .models import cluster_config as Cluster
from common.aes_decryptor import Prpcrypt
import pymysql as mdb



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
        pc = Prpcrypt()  # 初始化
        cluster.cluster_password = pc.decrypt(cluster.cluster_password)
    return clusters


def setClusterStatusByPort(port,stat):
    try:
        Cluster.objects.filter(cluster_port=int(port)).update(cluster_status=int(stat))
        return {'status': 0}
    except Exception as e:
        print(e)
        return {'status': 1}