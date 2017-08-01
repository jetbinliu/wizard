# -*- coding: UTF-8 -*-

import json
# import pymysql as mdb
import pymysql

from django.db.models import Q

from .models import mysql_cluster_config, redis_cluster_config, mongodb_cluster_config, mysql_cluster_metadata
from lib.mysqllib import mdb_query
from common.aes_decryptor import Prpcrypt

prpCryptor = Prpcrypt()  # 初始化


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


def getMySQLClusterDbs(host, port, user, password):
    # dbs = []
    # try:
    #     # Connect to the cluster database
    #     connection = mdb.connect(host=host,
    #                              port=port,
    #                              user=user,
    #                              passwd=passwd,
    #                              db='information_schema',
    #                              charset='utf8mb4',
    #                              cursorclass=mdb.cursors.DictCursor)
    #
    #     # with connection.cursor() as cursor:
    #     cursor = connection.cursor()
    sql = "select schema_name from schemata where schema_name not in (" \
          "'mysql','sys','information_schema','performance_schema')"
        # cursor.execute(sql)
        # results = cursor.fetchall()
    _, results = mdb_query(sql, host, port, user, password, 'information_schema', True)
    dbs = [result['schema_name'] for result in results]
    return dbs
    # except mdb.Warning as w:
    #     print(str(w))
    # except mdb.Error as e:
    #     print(str(e))
    # finally:
    #     connection.close()



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


# 采集集群元数据
def fetch_mysql_cluster_metadata():
    clusters = getAllMySQLInfo(cluster_role=1, flag='online')
    for cluster in clusters:
        cluster_name = cluster.cluster_name
        cluster_port = cluster.cluster_port
        # 获取从库连接信息，如果从库不存在则连接到主库查询
        dictSlaveConn = getSlaveConnStr(cluster_name)
        if dictSlaveConn:
            dictConn = dictSlaveConn
        else:
            dictConn = getMasterConnStr(cluster_name)
        Host = dictConn['Host']
        Port = dictConn['Port']
        User = dictConn['User']
        Password = dictConn['Password']
        # 去具体实例查询数据
        sqlContent = "select table_schema,table_name,table_type,engine,row_format,table_rows,avg_row_length," \
                     "data_length,max_data_length,index_length,data_free,auto_increment,create_time,table_collation," \
                     "create_options,table_comment from tables where table_schema not in {}".format(
            ('mysql', 'sys', 'mondmm', 'test', 'information_schema', 'performance_schema'),)
        cluster_db = "information_schema"
        _, results = mdb_query(sqlContent, Host, Port, User, Password, cluster_db, True)
        # 遍历然后查询建表语句
        for result in results:
            table_schema = result.get('table_schema')
            table_name =   result.get('table_name')
            _, res = mdb_query("show create table {}".format(table_name), Host, Port, User, Password, table_schema)
            create_statement = pymysql.escape_string(res[0][1])
            result['create_statement'] = create_statement
            # 元数据入库,如果存在就更新，如果不存在就插入(cluster_port, table_schema, table_name三个字段添加unique约束)
            metadatas = mysql_cluster_metadata.objects.filter(Q(cluster_port=cluster_port) & Q(table_schema=table_schema) & Q(table_name=table_name))
            if metadatas:
                metadata = metadatas[0]
            else:
                metadata = mysql_cluster_metadata()
            metadata.cluster_name = cluster_name
            metadata.cluster_port = cluster_port
            metadata.table_schema = result['table_schema']
            metadata.table_name = result['table_name']
            metadata.table_type = result['table_type']
            metadata.engine = result['engine']
            metadata.row_format = result['row_format']
            metadata.table_rows = result['table_rows'] if result['table_rows'] else 0
            metadata.avg_row_length = result['avg_row_length']
            metadata.data_length = result['data_length']
            metadata.max_data_length = result['max_data_length']
            metadata.index_length = result['index_length']
            metadata.data_free = result['data_free']
            metadata.auto_increment = result['auto_increment'] if result['auto_increment'] else 0
            metadata.create_time = result['create_time']
            metadata.table_collation = result['table_collation']
            metadata.create_statement = result['create_statement']
            metadata.create_options = result['create_options']
            metadata.table_comment = result['table_comment']
            metadata.save()



