# -*- coding: UTF-8 -*-

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .inceptionDal import InceptionDao
from dbconfig.dbconfigDal import getMasterConnStr

inceptionDao = InceptionDao()


# 提交工单前提交SQL给inception进行预检测
@csrf_exempt
def simplecheck(request):
    if request.is_ajax():
        sqlContent = request.POST.get('sql_content')
        clusterName = request.POST.get('cluster_name')
    else:
        sqlContent = request.POST['sql_content']
        clusterName = request.POST['cluster_name']

    finalResult = {'status': 0, 'msg': 'ok', 'data': []}
    # 服务器端参数验证
    if sqlContent is None or clusterName is None:
        finalResult['status'] = 1
        finalResult['msg'] = '页面提交参数可能为空'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')

    sqlContent = sqlContent.rstrip()
    if sqlContent[-1] != ";":
        finalResult['status'] = 1
        finalResult['msg'] = 'SQL语句结尾没有以;结尾，请重新修改并提交！'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')
    # 交给inception进行自动审核
    dictConn = getMasterConnStr(clusterName)
    result = inceptionDao.sqlautoReview(dictConn, sqlContent)
    if result is None or len(result) == 0:
        finalResult['status'] = 1
        finalResult['msg'] = '返回的结果集为空！可能是SQL语句有语法错误'
        return HttpResponse(json.dumps(finalResult), content_type='application/json')
    # 要把result转成JSON存进数据库里，方便SQL单子详细信息展示
    finalResult['data'] = result
    return HttpResponse(json.dumps(finalResult), content_type='application/json')
