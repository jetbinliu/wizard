# -*- coding: UTF-8 -*-

from collections import OrderedDict

from account.models import Users
from account.account_dao import getRoleById


leftMenuBtnsSuper = (
    {'key':'sysconfig', 'name':'系统管理', 'url':'', 'class':'glyphicon glyphicon-cog',
     'submenus':(
         {'key':'userconfig', 'name':'用户管理', 'url':'/account/index/', 'class': 'glyphicon glyphicon-user'},
        {'key':'masterconfig', 'name': '主库地址配置', 'url': '/admin/sql/master_config/', 'class': 'glyphicon glyphicon-user'},
        {'key':'userconfig', 'name': '用户权限配置', 'url': '/admin/sql/users/', 'class': 'glyphicon glyphicon-th-large'},
        {'key':'workflowconfig', 'name': '所有工单管理', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
    )},
)

leftMenuBtnsCommon = (
    {'key':'sysconfig', 'name':'SQL审核', 'url':'', 'class':'glyphicon glyphicon-asterisk',
     'submenus':(
        {'key': 'allworkflow', 'name': '查看历史工单', 'url': '/allworkflow/', 'class': 'glyphicon glyphicon-home'},
        {'key': 'submitsql', 'name': '发起SQL上线', 'url': '/submitsql/', 'class': 'glyphicon glyphicon-asterisk'},
        {'key': 'dbaprinciples', 'name': 'SQL审核必读', 'url': '/dbaprinciples/', 'class': 'glyphicon glyphicon-book'},
        {'key': 'charts', 'name': '统计图表展示', 'url': '/charts/', 'class': 'glyphicon glyphicon-file'},
    )},
     {'key':'logadmin', 'name':'日志管理', 'url':'', 'class':'glyphicon glyphicon-asterisk', 'submenus':(
        {'key': 'workflowconfig', 'name': '日你啊老赵', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
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