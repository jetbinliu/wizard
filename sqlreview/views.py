# -*- coding: UTF-8 -*-

import json

from django.shortcuts import render

from account.models import Users
from dbconfig.dbconfig_dao import getMySQLClusterDbs, getAllMySQLClusterInfo

# Create your views here.
def allworkflow(request):
    return render(request, 'sqlreview/allworkflow.html')

# 提交SQL的页面
def submitsql(request):
    # 获取所有在线集群信息
    clusters = getAllMySQLClusterInfo(flag='online')
    if len(clusters) == 0:
       context = {'errMsg': '在线MySQL集群数为0, 可能后端数据没有配置集群！'}
       return render(request, 'sqlreview/error.html', context)

    # 获取所有集群名称
    listAllClusterName = [cluster.cluster_name for cluster in clusters]
    # 转换为集合（间接去重）
    setAllClusterName = set(listAllClusterName)
    if len(setAllClusterName) < len(listAllClusterName):
        context = {'errMsg': '存在两个集群名称一样的集群，请修改数据库'}
        return render(request, 'sqlreview/error.html', context)

    # cluster_hosts列表0号位为主库地址, 登录获取databaase列表
    dictAllClusterDb = {}
    for cluster in clusters:
        try:
            dbs = getMySQLClusterDbs(
                json.loads(cluster.cluster_hosts)[0], cluster.cluster_port,
                cluster.cluster_user, cluster.cluster_password
            )
            dictAllClusterDb[cluster.cluster_name] = dbs
        except Exception as e:
            context = {'errMsg': '%s' % e}
            return render(request, 'sqlreview/error.html', context)

    # 获取所有审核人(超级管理员、管理员、DBA、leader、项目管理)，当前登录用户不可以审核自己的工单
    loginUser = request.session.get('login_username')
    reviewMen = Users.objects.values('username','email','role').filter(role__lte=5).exclude(username=loginUser)
    if len(reviewMen) == 0:
       context = {'errMsg': '审核人为0, 请配置审核人。'}
       return render(request, 'sqlreview/error.html', context)

    context = {
        'dictAllClusterDb': dictAllClusterDb,
        'reviewMen': reviewMen
    }
    return render(request, 'sqlreview/submitsql.html', context)


# 提交SQL给inception进行解析
def autoreview(request):
    sqlContent = request.POST['sql_content']
    workflowName = request.POST['workflow_name']
    clusterName = request.POST['cluster_name']
    isBackup = request.POST['is_backup']
    reviewMan = request.POST['review_man']

    # 服务器端参数验证
    if sqlContent is None or workflowName is None or clusterName is None or isBackup is None or reviewMan is None:
        context = {'errMsg': '页面提交参数可能为空'}
        return render(request, 'error.html', context)
    sqlContent = sqlContent.rstrip()
    if sqlContent[-1] != ";":
        context = {'errMsg': "SQL语句结尾没有以;结尾，请后退重新修改并提交！"}
        return render(request, 'error.html', context)

    # 交给inception进行自动审核
    result = inceptionDao.sqlautoReview(sqlContent, clusterName, isBackup)
    if result is None or len(result) == 0:
        context = {'errMsg': 'inception返回的结果集为空！可能是SQL语句有语法错误'}
        return render(request, 'error.html', context)
    # 要把result转成JSON存进数据库里，方便SQL单子详细信息展示
    jsonResult = json.dumps(result)

    # 遍历result，看是否有任何自动审核不通过的地方，一旦有，则为自动审核不通过；没有的话，则为等待人工审核状态
    workflowStatus = Const.workflowStatus['manreviewing']
    for row in result:
        if row[2] == 2:
            # 状态为2表示严重错误，必须修改
            workflowStatus = Const.workflowStatus['autoreviewwrong']
            break
        elif re.match(r"\w*comments\w*", row[4]):
            workflowStatus = Const.workflowStatus['autoreviewwrong']
            break

    # 存进数据库里
    engineer = request.session.get('login_username', False)
    newWorkflow = workflow()
    newWorkflow.workflow_name = workflowName
    newWorkflow.engineer = engineer
    newWorkflow.review_man = reviewMan
    newWorkflow.create_time = getNow()
    newWorkflow.status = workflowStatus
    newWorkflow.is_backup = isBackup
    newWorkflow.review_content = jsonResult
    newWorkflow.cluster_name = clusterName
    newWorkflow.sql_content = sqlContent
    newWorkflow.save()
    workflowId = newWorkflow.id

    # 自动审核通过了，才发邮件
    if workflowStatus == Const.workflowStatus['manreviewing']:
        # 如果进入等待人工审核状态了，则根据settings.py里的配置决定是否给审核人发一封邮件提醒.
        if hasattr(settings, 'MAIL_ON_OFF') == True:
            if getattr(settings, 'MAIL_ON_OFF') == "on":
                url = _getDetailUrl(request) + str(workflowId) + '/'

                # 发一封邮件
                strTitle = "新的SQL上线工单提醒 # " + str(workflowId)
                strContent = "发起人：" + engineer + "\n审核人：" + reviewMan + "\n工单地址：" + url + "\n工单名称： " + workflowName + "\n具体SQL：" + sqlContent
                objEngineer = users.objects.get(username=engineer)
                objReviewMan = users.objects.get(username=reviewMan)
                mailSender.sendEmail(strTitle, strContent, [objReviewMan.email])
            else:
                # 不发邮件
                pass

    return HttpResponseRedirect('/detail/' + str(workflowId) + '/')
