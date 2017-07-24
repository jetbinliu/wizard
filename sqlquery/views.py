# -*- coding: UTF-8 -*-

import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from account.models import Users
from dbconfig.dbconfigDal import getMySQLClusterDbs, getAllMySQLInfo, getMasterConnStr, getSlaveConnStr
from .models import workflow
from lib.mysqllib import mdb_query
from lib.util import DateTimeEncoder
from lib.configgetter import Configuration
from common.aes_decryptor import Prpcrypt

conf = Configuration("conf/global.conf")
prpCryptor = Prpcrypt()  # 初始化


# Create your views here.
# 首页，也是查看所有SQL工单页面，具备翻页功能
def allworkflow(request):
    # 一个页面展示
    PAGE_LIMIT = 10

    pageNo = 0
    navStatus = 0
    listAllWorkflow = []

    # 参数检查
    if 'pageNo' in request.GET:
        pageNo = request.GET['pageNo']
    else:
        pageNo = '0'

    if 'navStatus' in request.GET:
        navStatus = request.GET['navStatus']
    else:
        navStatus = 'all'
    if not isinstance(pageNo, str) or not isinstance(navStatus, str):
        raise TypeError('pageNo或navStatus页面传入参数不对')
    else:
        try:
            pageNo = int(pageNo)
            if pageNo < 0:
                pageNo = 0
        except ValueError as ve:
            context = {'errMsg': 'pageNo参数不是int.'}
            return render(request, 'error.html', context)

    loginUser = request.session.get('login_username')
    # 查询workflow model，根据pageNo和navStatus获取对应的内容
    offset = pageNo * PAGE_LIMIT
    limit = offset + PAGE_LIMIT

    listWorkflow = []
    # 查询全部流程
    roleLeve = int(conf.get("sqlabout", 'roleLeve'))
    loginUserOb = Users.objects.get(username=loginUser)
    if navStatus == 'all' and loginUserOb.role <= roleLeve:
        # 这句话等同于select * from sql_workflow order by create_time desc limit {offset, limit};
        listWorkflow = workflow.objects.order_by('-create_time')[offset:limit]
    elif navStatus == 'all' and loginUserOb.role > roleLeve:
        listWorkflow = workflow.objects.filter(engineer=loginUser).order_by('-create_time')[offset:limit]

    context = {
        'listWorkflow': listWorkflow,
    }
    return render(request, 'sqlquery/allworkflow.html', context)

def submitsql(request):
    # 获取所有在线集群信息
    clusters = getAllMySQLInfo(cluster_role=1, flag='online')
    if len(clusters) == 0:
       context = {'errMsg': '在线MySQL集群数为0, 可能后端数据没有配置集群！'}
       return render(request, 'error.html', context)

    # cluster_role 0 为主库, 登录获取databaase列表
    dictAllClusterDb = {}
    for cluster in clusters:
        try:
            dbs = getMySQLClusterDbs(
                cluster.cluster_host, cluster.cluster_port,
                cluster.cluster_user, cluster.cluster_password
            )
            dictAllClusterDb[cluster.cluster_name] = dbs
        except Exception as e:
            context = {'errMsg': u'连接到从库 %s:%d 失败: %s' % (cluster.cluster_host, cluster.cluster_port, e)}
            return render(request, 'error.html', context)

    context = {
        'dictAllClusterDb': dictAllClusterDb,
    }
    return render(request, 'sqlquery/submitsql.html', context)

def autoquery(request):
    workflowName = request.POST['workflow_name']
    clusterName = request.POST['cluster_name']
    cluster_db = request.POST.get('cluster_db')
    sqlContent = request.POST['sql_content']

    # 服务器端参数验证
    if not workflowName or not clusterName or not cluster_db or not sqlContent:
        context = {'errMsg': '页面提交参数可能为空'}
        return render(request, 'error.html', context)
    sqlContent = sqlContent.strip()
    if sqlContent[-1] != ";":
        sqlContent = sqlContent + ";"

    # 获取当前登录用户作为工单发起人
    engineer = request.session.get('login_username', False)

    # 获取从库连接信息，如果从库不存在则连接到主库
    dictSlaveConn = getSlaveConnStr(clusterName)
    if dictSlaveConn:
        dictConn = dictSlaveConn
    else:
        dictConn = getMasterConnStr(clusterName)
    Host = dictConn['Host']
    Port = dictConn['Port']
    User = dictConn['User']
    Password = dictConn['Password']

    # 去具体实例查询数据
    field_names, results = mdb_query(sqlContent, Host, Port, User, Password, cluster_db)
    field_names = field_names if field_names else []
    results = results if results else []
    # 进行脱敏处理：对用户手机号、身份证号、银行卡号进行加密
    sensitive_fields = json.loads(conf.get("sqlabout", 'sensitive_fields'))
    for result in results:
        for index, item in enumerate(field_names):
            if item in sensitive_fields:
                result[index] = 'pbkdf2_sha256$' + prpCryptor.encrypt(result[index]).decode('utf-8')


    Workflow = workflow()
    Workflow.workflow_name = workflowName
    Workflow.cluster_name = clusterName
    Workflow.engineer = engineer
    Workflow.cluster_db = cluster_db
    Workflow.sql_content = sqlContent
    Workflow.field_names = json.dumps(field_names)
    Workflow.query_result = json.dumps(results, cls=DateTimeEncoder)
    Workflow.save()
    workflowId = Workflow.id

    return HttpResponseRedirect('/sqlquery/detail/' + str(workflowId) + '/')

# 展示SQL工单详细内容，以及可以人工审核，审核通过即可执行
def detail(request, workflowId):
    # 根据workflowId去db里检索工单
    workflowDetail = get_object_or_404(workflow, pk=workflowId)
    workflowDetail.field_names = json.loads(workflowDetail.field_names)
    workflowDetail.query_result = json.loads(workflowDetail.query_result)

    context = {
        'workflowDetail': workflowDetail,
    }
    return render(request, 'sqlquery/detail.html', context)


