# -*- coding: UTF-8 -*-

import re
import json
import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

from account.models import Users
from dbconfig.dbconfigDal import getMySQLClusterDbs, getAllMySQLClusterInfo, getMasterConnStr
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

    context = {
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
    workflowid =  request.POST.get('workflowid')  # 扩充的工单驳回修改功能
    sqlContent = request.POST['sql_content']
    workflowName = request.POST['workflow_name']
    clusterName = request.POST['cluster_name']
    isBackup = request.POST['is_backup']
    reviewMan = request.POST['review_man']
    subReviewMan = request.POST.get('sub_review_man', '')

    reviewMans = [reviewMan, subReviewMan]


    # 服务器端参数验证
    if sqlContent is None or workflowName is None or clusterName is None or isBackup is None or reviewMan is None:
        context = {'errMsg': '页面提交参数可能为空'}
        return render(request, 'sqlreview/error.html', context)
    sqlContent = sqlContent.strip()
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
        # if row[2] == 2:
        #     # 状态为2表示严重错误，必须修改
        #     workflowStatus = 2
        #     break
        # elif re.match(r"\w*comments\w*", row[4]):
        #     # 没有注释
        #     workflowStatus = 2
        #     break
        if row[2] != 0:
            workflowStatus = 2
            break


    # 获取当前登录用户作为工单发起人
    engineer = request.session.get('login_username', False)

    # 发起新工单
    if not workflowid:
        Workflow = workflow()
        Workflow.create_time = getNow()
    # 修改后再次提交的工单,保留原本的创建时间
    else:
        Workflow = workflow.objects.get(id=int(workflowid))

    Workflow.workflow_name = workflowName
    Workflow.engineer = engineer
    Workflow.review_man = json.dumps(reviewMans)  # 把主审核人reviewMan、副审核人subReviewMan转成JSON存进数据库里
    Workflow.status = workflowStatus
    Workflow.is_backup = isBackup
    Workflow.review_content = jsonResult
    Workflow.cluster_name = clusterName
    Workflow.sql_content = sqlContent
    Workflow.save()
    workflowId = Workflow.id

    # 自动审核通过了，才发邮件
    if workflowStatus == 3:
        # 如果进入等待人工审核状态了，则根据global.conf里的配置决定是否给审核人发一封邮件提醒.
        if conf.has_option("INCEPTION", 'MAIL_ON_OFF'):
            if conf.get("INCEPTION", 'MAIL_ON_OFF').lower() == "on":
                url = _getDetailUrl(request) + str(workflowId) + '/'

                # 发一封邮件
                strTitle = "新的SQL上线工单提醒 # " + str(workflowId)
                strContent = "发起人：" + engineer + "\n审核人：" + " ".join(reviewMans) + "\n工单地址：" + url + "\n工单名称： " + workflowName + "\n具体SQL：" + sqlContent
                # objEngineer = Users.objects.get(username=engineer)
                # 发邮件通知主副审核人
                for _review_man in reviewMans:
                    if _review_man:
                        objReviewMan = Users.objects.get(username=_review_man)
                        mailSender.sendEmail(strTitle, strContent, [objReviewMan.email])
            else:
                # 不发邮件
                pass

    return HttpResponseRedirect('/sqlreview/detail/' + str(workflowId) + '/')


#展示SQL工单详细内容，以及可以人工审核，审核通过即可执行
def detail(request, workflowId):
    # 根据workflowId去db里检索工单
    workflowDetail = get_object_or_404(workflow, pk=workflowId)
    workflowDetail.status = WORKFLOW_STATUS[workflowDetail.status]
    reviewMans = json.loads(workflowDetail.review_man)
    notes = json.loads(workflowDetail.notes)

    # 服务器端二次验证，如果正在查看工单详情的当前登录用户，不是发起人，也不属于审核人群，则异常.
    loginUser = request.session.get('login_username', False)
    authorizedGroups = [workflowDetail.engineer, "admin"]
    authorizedGroups.extend(reviewMans)
    if loginUser is None or loginUser not in authorizedGroups:
        context = {'errMsg': '当前登录用户不是发起人，也不属于审核人群，请重新登录.'}
        return render(request, 'sqlreview/error.html', context)

    listContent = None
    if workflowDetail.status in ('执行有异常', '已正常结束'):
        listContent = json.loads(workflowDetail.execute_result)
    else:
        listContent = json.loads(workflowDetail.review_content)
    context = {
               'workflowDetail': workflowDetail,
               'reviewMans': reviewMans,
               'listContent': listContent,
               'notes': notes,
               }
    return render(request, 'sqlreview/detail.html', context)



# 发起人终止流程
def cancel(request):
    workflowId = request.POST['workflowid']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空.'}
        return render(request, 'sqlreview/error.html', context)

    workflowId = int(workflowId)
    workflowDetail = workflow.objects.get(id=workflowId)

    # 服务器端二次验证，如果正在执行终止动作的当前登录用户，不是发起人，则异常.
    loginUser = request.session.get('login_username', False)
    if loginUser is None or loginUser != workflowDetail.engineer:
        context = {'errMsg': '当前登录用户不是发起人，请重新登录.'}
        return render(request, 'sqlreview/error.html', context)

    # 服务器端二次验证，如果当前单子状态不是等待审核人审核状态，则不能发起终止.
    if workflowDetail.status != 3:
        context = {'errMsg': '当前单子状态不是等待审核人审核状态，则不能发起终止.'}
        return render(request, 'sqlreview/error.html', context)

    workflowDetail.finish_time = getNow()
    workflowDetail.status = 4
    workflowDetail.save()
    return HttpResponseRedirect('/sqlreview/detail/' + str(workflowId) + '/')

# 审核人驳回工单
def reject(request):
    workflowId = request.POST['workflowid']
    rejectOpinion = request.POST['reject_opinion']
    rejectedMan = request.POST['rejected_man']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空.'}
        return render(request, 'sqlreview/error.html', context)

    workflowId = int(workflowId)
    workflowDetail = workflow.objects.get(id=workflowId)

    # 服务器端二次验证，如果正在执行驳回动作的当前登录用户，不是审核人，则异常.
    loginUser = request.session.get('login_username', False)
    if loginUser is None or loginUser not in json.loads(workflowDetail.review_man):
        context = {'errMsg': '当前登录用户不是审核人，请重新登录.'}
        return render(request, 'sqlreview/error.html', context)

    # 服务器端二次验证，如果当前单子状态不是等待审核人审核状态，则不能发起驳回.
    if workflowDetail.status != 3:
        context = {'errMsg': '当前单子状态不是等待审核人审核状态，则不能发起终止.'}
        return render(request, 'sqlreview/error.html', context)

    #驳回工单审核人用户名
    d = json.loads(workflowDetail.notes)
    d['rejected_man'] = rejectedMan

    workflowDetail.status = 5
    workflowDetail.reject_opinion = rejectOpinion
    workflowDetail.notes = json.dumps(d)
    workflowDetail.save()

    # 如果人工终止了，则根据global.conf里的配置决定是否给提交者一封邮件提醒，并附带说明此单子被拒绝掉了，需要重新修改.
    if conf.has_option("INCEPTION", 'MAIL_ON_OFF'):
        # 判断setting内容和当前登陆用户，如果为提交者自己终止的时候是不需要发邮件的
        if conf.get("INCEPTION", 'MAIL_ON_OFF') == "on" and loginUser != workflowDetail.engineer:
            url = _getDetailUrl(request) + str(workflowId) + '/'

            # 发一封邮件
            engineer = workflowDetail.engineer
            reviewMan = workflowDetail.review_man
            workflowStatus = WORKFLOW_STATUS[workflowDetail.status]
            workflowName = workflowDetail.workflow_name
            objEngineer = users.objects.get(username=engineer)
            # objReviewMan = users.objects.get(username=reviewMan)
            strTitle = "SQL上线工单被拒绝执行 # " + str(workflowId)
            strContent = "发起人：" + engineer + "\n审核人：" + reviewMan + "\n工单地址：" + url + "\n工单名称： " + workflowName + "\n执行结果：" + workflowStatus + "\n提醒：此工单被拒绝执行，请登陆按照规范重新修改并重新提交"
            mailSender.sendEmail(strTitle, strContent, [objEngineer.email])
        else:
            # 不发邮件
            pass

    return HttpResponseRedirect('/sqlreview/detail/' + str(workflowId) + '/')


def editsql(request, workflowId):
    # 根据workflowId去db里检索工单
    workflowDetail = get_object_or_404(workflow, pk=workflowId)
    sqlContent = workflowDetail.sql_content.strip()

    # 服务器端二次验证，如果正在执行修改动作的当前登录用户，不是发起人，则异常.
    loginUser = request.session.get('login_username', False)
    if loginUser is None or loginUser != workflowDetail.engineer:
        context = {'errMsg': '当前登录用户不是发起人，请重新登录.'}
        return render(request, 'sqlreview/error.html', context)

    # 服务器端二次验证，如果当前单子状态不是等待审核人审核状态，则不能发起驳回.
    if workflowDetail.status not in (2, 4, 5, 7):
        context = {'errMsg': '当前单子状态不是: 自动审核不通过、发起人终止、审核人驳回、执行有异常等状态，则不能发起修改.'}
        return render(request, 'sqlreview/error.html', context)


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
               'workflowDetail': workflowDetail,
               'sqlContent': sqlContent,
               'dictAllClusterDb': dictAllClusterDb,
               'reviewMen': reviewMen,
               }
    return render(request, 'sqlreview/submitsql.html', context)


# 人工审核也通过，执行SQL
def execute(request):
    workflowId = request.POST['workflowid']
    reviewedMan = request.POST['reviewed_man']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空.'}
        return render(request, 'sqlreview/error.html', context)

    workflowId = int(workflowId)
    workflowDetail = workflow.objects.get(id=workflowId)
    clusterName = workflowDetail.cluster_name
    reviewMans = json.loads(workflowDetail.review_man)

    # 服务器端二次验证，正在执行人工审核动作的当前登录用户必须为审核人. 避免攻击或被接口测试工具强行绕过
    loginUser = request.session.get('login_username', False)
    if loginUser is None or loginUser not in reviewMans:
        context = {'errMsg': '当前登录用户不是审核人，请重新登录.'}
        return render(request, 'sqlreview/error.html', context)

    # 服务器端二次验证，当前工单状态必须为等待人工审核
    if workflowDetail.status != 3:
        context = {'errMsg': '当前工单状态不是等待人工审核中，请刷新当前页面！'}
        return render(request, 'sqlreview/error.html', context)

    # 审核通过工单审核人用户名
    d = json.loads(workflowDetail.notes)
    d['reviewed_man'] = reviewedMan

    # 将流程状态修改为执行中，并更新reviewok_time字段
    workflowDetail.status = 6
    workflowDetail.reviewok_time = getNow()
    workflowDetail.notes = json.dumps(d)
    workflowDetail.save()

    # 交给inception先split，再执行
    dictConn = getMasterConnStr(clusterName)
    (finalStatus, finalList) = inceptionDao.executeFinal(workflowDetail, dictConn)

    # 封装成JSON格式存进数据库字段里
    strJsonResult = json.dumps(finalList)
    workflowDetail.execute_result = strJsonResult
    workflowDetail.finish_time = getNow()
    workflowDetail.status = finalStatus
    workflowDetail.save()

    # 如果执行完毕了，则根据settings.py里的配置决定是否给提交者和DBA一封邮件提醒.DBA需要知晓审核并执行过的单子
    if conf.has_option("INCEPTION", 'MAIL_ON_OFF'):
        if conf.get("INCEPTION", 'MAIL_ON_OFF').lower() == "on":
            url = _getDetailUrl(request) + str(workflowId) + '/'

            # 发一封邮件
            engineer = workflowDetail.engineer
            reviewMan = workflowDetail.review_man
            workflowStatus = WORKFLOW_STATUS[workflowDetail.status]
            workflowName = workflowDetail.workflow_name
            objEngineer = Users.objects.get(username=engineer)
            # objReviewMan = users.objects.get(username=reviewMan)
            strTitle = "SQL上线工单执行完毕 # " + str(workflowId)
            strContent = "发起人：" + engineer + "\n审核人：" + " ".join(reviewMans) + "\n工单地址：" + url + "\n工单名称： " + workflowName + "\n执行结果：" + workflowStatus
            mailSender.sendEmail(strTitle, strContent, [objEngineer.email])
            mailSender.sendEmail(strTitle, strContent, getattr(settings, 'MAIL_REVIEW_DBA_ADDR'))
        else:
            # 不发邮件
            pass

    return HttpResponseRedirect('/sqlreview/detail/' + str(workflowId) + '/')


#展示回滚的SQL
def rollbacksql(request):
    workflowId = request.GET['workflowid']
    if workflowId == '' or workflowId is None:
        context = {'errMsg': 'workflowId参数为空.'}
        return render(request, 'sqlreview/error.html', context)
    workflowId = int(workflowId)
    listBackupSql = inceptionDao.getRollbackSqlList(workflowId)

    context = {'listBackupSql':listBackupSql}
    return render(request, 'rollbacksql.html', context)



#获取当前时间
def getNow():
    NOW = datetime.datetime.now()
    return datetime.datetime.strftime(NOW, "%Y-%m-%d %H:%M:%S")

#获取当前请求url
def _getDetailUrl(request):
    scheme = request.scheme
    host = request.META['HTTP_HOST']
    return "%s://%s/detail/" % (scheme, host)