# -*- coding: UTF-8 -*-

import json

from django.db import connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from common.aes_decryptor import Prpcrypt

prpCryptor = Prpcrypt()  # 初始化


@csrf_exempt
def desensitization(request):
    if request.is_ajax():
        encrypted_field = request.POST.get("encrypted_field")
    else:
        encrypted_field = request.POST['encrypted_field']
    _encrypted_field = encrypted_field[14:]
    decrypt_field = prpCryptor.decrypt(_encrypted_field)
    result = {'status':0, 'msg':'ok', 'data':decrypt_field}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def getDbsFromClusterName(request):
    if request.is_ajax():
        cluster_name = request.POST.get("cluster_name")
    else:
        cluster_name = request.POST['cluster_name']

    cursor = connection.cursor()
    cursor.execute("select distinct table_schema from dbconfig_mysql_cluster_metadata where cluster_name=%s", (cluster_name,))
    dbs = [db[0] for db in cursor.fetchall()]
    cursor.close()

    result = {'status':0, 'msg':'ok', 'data':dbs}
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def getTablesFromDb(request):
    if request.is_ajax():
        table_schema = request.POST.get("table_schema")
    else:
        table_schema = request.POST.get("table_schema")

    cursor = connection.cursor()
    cursor.execute("select table_name,table_comment from dbconfig_mysql_cluster_metadata where table_schema=%s", (table_schema,))
    tbs = cursor.fetchall()
    cursor.close()

    result = {'status':0, 'msg':'ok', 'data':tbs}
    return HttpResponse(json.dumps(result), content_type='application/json')










