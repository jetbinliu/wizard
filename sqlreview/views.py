# -*- coding: UTF-8 -*-

import re
import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from account.models import Users
from dbconfig.dbconfigDal import getMySQLClusterDbs, getAllMySQLClusterInfo
from .inceptionDal import InceptionDao
from .models import workflow, WORKFLOW_STATUS
from lib.configgetter import Configuration

conf = Configuration("conf/global.conf")
inceptionDao = InceptionDao()

# Create your views here.

# 首页，也是查看所有SQL工单页面，具备翻页功能
def allworkflow(request):
    # 一个页面展示
    PAGE_LIMIT = 12

    pageNo = 0
    navStatus = ''
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
            return render(request, 'sqlreview/error.html', context)

    loginUser = request.session.get('login_username')
    # 查询workflow model，根据pageNo和navStatus获取对应的内容
    offset = pageNo * PAGE_LIMIT
    limit = offset + PAGE_LIMIT

    # 修改全部工单、审核不通过、已执行完毕界面工程师只能看到自己发起的工单，审核人可以看到全部
    listWorkflow = []
    # 查询全部流程
    loginUserOb = Users.objects.get(username=loginUser)
    if navStatus == 'all' and loginUserOb.role <= 5:
        # 这句话等同于select * from sql_workflow order by create_time desc limit {offset, limit};
        listWorkflow = workflow.objects.exclude(status=2).order_by(
            '-create_time')[offset:limit]
    elif navStatus == 'all' and loginUserOb.role == '工程师':
        listWorkflow = workflow.objects.filter(
            Q(engineer=loginUser) | Q(status=2), engineer=loginUser).order_by(
            '-create_time')[offset:limit]
    elif navStatus == 'waitingforme':
        listWorkflow = workflow.objects.filter(status=3,
                                               review_man=loginUser).order_by('-create_time')[offset:limit]
    elif navStatus == 'finish' and loginUserOb.role == '审核人':
        listWorkflow = workflow.objects.filter(status=8).order_by('-create_time')[
                       offset:limit]
    elif navStatus == 'finish' and loginUserOb.role == '工程师':
        listWorkflow = workflow.objects.filter(status=8, engineer=loginUser).order_by(
            '-create_time')[offset:limit]
    elif navStatus == 'autoreviewwrong' and loginUserOb.role == '审核人':
        listWorkflow = workflow.objects.filter(status=2).order_by('-create_time')[
                       offset:limit]
    elif navStatus == 'autoreviewwrong' and loginUserOb.role == '工程师':
        listWorkflow = workflow.objects.filter(status=2,
                                               engineer=loginUser).order_by('-create_time')[offset:limit]
    else:
        context = {'errMsg': '传入的navStatus参数有误！'}
        return render(request, 'sqlreview/error.html', context)

    context = {'currentMenu': 'allworkflow',
               'listWorkflow': listWorkflow,
               'WORKFLOW_STATUS': WORKFLOW_STATUS,
               'pageNo': pageNo,
               'navStatus': navStatus,
               'PAGE_LIMIT': PAGE_LIMIT}
    return render(request, 'sqlreview/allworkflow.html', context)

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
    subReviewMan = request.POST.get('sub_review_man', '')

    # 服务器端参数验证
    if sqlContent is None or workflowName is None or clusterName is None or isBackup is None or reviewMan is None:
        context = {'errMsg': '页面提交参数可能为空'}
        return render(request, 'sqlreview/error.html', context)
    sqlContent = sqlContent.rstrip()
    if sqlContent[-1] != ";":
        context = {'errMsg': "SQL语句结尾没有以;结尾，请后退重新修改并提交！"}
        return render(request, 'sqlreview/error.html', context)

    # 交给inception进行自动审核
    result = inceptionDao.sqlautoReview(sqlContent, clusterName, isBackup)
    if result is None or len(result) == 0:
        context = {'errMsg': 'inception返回的结果集为空！可能是SQL语句有语法错误'}
        return render(request, 'sqlreview/error.html', context)
    # 要把result转成JSON存进数据库里，方便SQL单子详细信息展示
    jsonResult = json.dumps(result)

    # 遍历result，看是否有任何自动审核不通过的地方，一旦有，则为自动审核不通过；没有的话，则为等待人工审核状态
    workflowStatus = 3
    for row in result:
        if row[2] == 2:
            # 状态为2表示严重错误，必须修改
            workflowStatus = 2
            break
        elif re.match(r"\w*comments\w*", row[4]):
            workflowStatus = 2
            break

    # 存进数据库里
    engineer = request.session.get('login_username', False)
    newWorkflow = workflow()
    newWorkflow.workflow_name = workflowName
    newWorkflow.engineer = engineer
    newWorkflow.review_man = json.dumps([reviewMan, subReviewMan])  # 把主审核人reviewMan、副审核人subReviewMan转成JSON存进数据库里
    newWorkflow.create_time = getNow()
    newWorkflow.status = workflowStatus
    newWorkflow.is_backup = isBackup
    newWorkflow.review_content = jsonResult
    newWorkflow.cluster_name = clusterName
    newWorkflow.sql_content = sqlContent
    newWorkflow.save()
    workflowId = newWorkflow.id

    # 自动审核通过了，才发邮件
    if workflowStatus == 3:
        # 如果进入等待人工审核状态了，则根据settings.py里的配置决定是否给审核人发一封邮件提醒.
        if conf.has_option("INCEPTION", 'MAIL_ON_OFF'):
            if conf.get("INCEPTION", 'MAIL_ON_OFF').lower() == "on":
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

    return HttpResponseRedirect('/sqlreview/detail/' + str(workflowId) + '/')


#展示SQL工单详细内容，以及可以人工审核，审核通过即可执行
def detail(request, workflowId):
    workflowDetail = get_object_or_404(workflow, pk=workflowId)
    listContent = None
    if workflowDetail.status in (7, 8):
        listContent = json.loads(workflowDetail.execute_result)
    else:
        listContent = json.loads(workflowDetail.review_content)
    context = {'currentMenu':'allworkflow',
               'workflowDetail':workflowDetail,
               'WORKFLOW_STATUS': WORKFLOW_STATUS,
               'listContent':listContent}
    return render(request, 'sqlreview/detail.html', context)



#获取当前时间
def getNow():
    NOW = datetime.datetime.now()
    return datetime.datetime.strftime(NOW, "%Y-%m-%d %H:%M:%S")

#获取当前请求url
def _getDetailUrl(request):
    scheme = request.scheme
    host = request.META['HTTP_HOST']
    return "%s://%s/detail/" % (scheme, host)