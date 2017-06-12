# -*- coding: UTF-8 -*-

from collections import OrderedDict

from account.models import Users
from account.account_dao import getRoleById


leftMenuBtnsSuper = (
    {'key':'sysconfig', 'name':'系统管理', 'url':'', 'class':'glyphicon glyphicon-cog',
     'submenus':(
        {'key':'userconfig', 'name':'用户管理', 'url':'/account/index/', 'class': 'glyphicon glyphicon-user'},
        {'key':'userauthority', 'name': '用户权限配置', 'url': '#', 'class': 'glyphicon glyphicon-wrench'},
    )},
    {'key': 'dbconfig', 'name': '数据库管理', 'url': '', 'class': 'glyphicon glyphicon-oil',
     'submenus': (
         {'key': 'masterconfig', 'name': '主库地址配置', 'url': '/dbconfig/index/', 'class': 'glyphicon glyphicon-user'},
     )},
    {'key': 'dbconfig', 'name': '工单管理', 'url': '', 'class': 'glyphicon glyphicon-th-list',
     'submenus': (
         {'key': 'workflowconfig', 'name': 'SQL审核工单管理', 'url': '#', 'class': 'glyphicon glyphicon-list-alt'},
     )},
)

leftMenuBtnsCommon = (
    {'key':'sysconfig', 'name':'SQL审核', 'url':'', 'class':'glyphicon glyphicon-tint',
     'submenus':(
        {'key': 'allworkflow', 'name': '查看历史工单', 'url': '/sqlreview/allworkflow/', 'class': 'glyphicon glyphicon-home'},
        {'key': 'submitsql', 'name': '发起SQL上线', 'url': '/sqlreview/submitsql/', 'class': 'glyphicon glyphicon-asterisk'},
        {'key': 'dbaprinciples', 'name': 'SQL审核必读', 'url': '/dbaprinciples/', 'class': 'glyphicon glyphicon-book'},
        {'key': 'charts', 'name': '统计图表展示', 'url': '/charts/', 'class': 'glyphicon glyphicon-file'},
    )},
     {'key':'logadmin', 'name':'日志管理', 'url':'', 'class':'glyphicon glyphicon-hdd', 'submenus':(
        {'key': 'workflowconfig', 'name': '日你啊老赵', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
        {'key': 'workflowconfig', 'name': '日你啊老王 ', 'url': '/admin/sql/workflow/',
         'class': 'glyphicon glyphicon-list-alt'},
        {'key': 'workflowconfig', 'name': '日你啊李丁', 'url': '/admin/sql/workflow/',
         'class': 'glyphicon glyphicon-list-alt'},
    )},
)

leftMenuBtnsDoc = (

)







def messages(request):
    """存放用户，会话信息等."""
    loginUser = request.session.get('login_username')
    if loginUser is not None:
        user = Users.objects.get(username=loginUser)
        user.role = getRoleById(user.role)
        if user.is_superuser:
            # leftMenuBtns = leftMenuBtnsSuper + leftMenuBtnsCommon + leftMenuBtnsDoc
            leftMenuBtns = leftMenuBtnsSuper + leftMenuBtnsCommon
        else:
            # leftMenuBtns = leftMenuBtnsCommon + leftMenuBtnsDoc
            leftMenuBtns = leftMenuBtnsCommon
    else:
        user = None
        leftMenuBtns = ()

    context = {
        'user': user,
        'leftMenuBtns': leftMenuBtns,
    }
    return context