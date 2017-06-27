# -*- coding: UTF-8 -*-

# from collections import OrderedDict

from account.models import Users
from account.accountDal import getRoleById


leftMenuBtnsSuper = (
    {'name':'系统管理', 'url':'', 'class':'glyphicon glyphicon-cog',
     'submenus':(
        {'name':'用户管理', 'url':'/account/index/', 'class': 'glyphicon glyphicon-user'},
        {'name': '用户权限配置', 'url': '#', 'class': 'glyphicon glyphicon-wrench'},
    )},
    {'name': '数据库管理', 'url': '', 'class': 'glyphicon glyphicon-oil',
     'submenus': (
         {'name': 'MySQL集群', 'url': '/dbconfig/MySQL-Cluster/', 'class': 'glyphicon glyphicon-user'},
         {'name': 'Redis集群', 'url': '/dbconfig/Redis-Cluster/', 'class': 'glyphicon glyphicon-user'},
         {'name': 'MongoDB集群', 'url': '/dbconfig/MongoDB-Cluster/', 'class': 'glyphicon glyphicon-user'},
     )},
)

leftMenuBtnsCommon = (
    {'name':'SQL审核', 'url':'', 'class':'glyphicon glyphicon-tint',
     'submenus':(
        {'name': '查看历史工单', 'url': '/sqlreview/allworkflow/', 'class': 'glyphicon glyphicon-home'},
        {'name': '发起SQL上线', 'url': '/sqlreview/submitsql/', 'class': 'glyphicon glyphicon-asterisk'},
        {'name': 'SQL审核必读', 'url': '/dbaprinciples/', 'class': 'glyphicon glyphicon-book'},
        {'name': '统计图表展示', 'url': '/charts/', 'class': 'glyphicon glyphicon-file'},
    )},
    {'name': '备份管理', 'url': '/dbconfig/index/', 'class': 'glyphicon glyphicon-user',
     'submenus': (
         {'name': 'MySQL备份', 'url': '/bakconfig/mysqlbackup/', 'class': 'glyphicon glyphicon-wrench'},
         {'name': 'Redis备份', 'url': '#', 'class': 'glyphicon glyphicon-wrench'},
         {'name': 'MongoDB备份', 'url': '#', 'class': 'glyphicon glyphicon-wrench'},
     )},
    {'name': '日志管理', 'url': '', 'class': 'glyphicon glyphicon-hdd', 'submenus': (
        {'name': '日你啊老赵', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
        {'name': '日你啊老王 ', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
        {'name': '日你啊李丁', 'url': '/admin/sql/workflow/', 'class': 'glyphicon glyphicon-list-alt'},
    )},
    {'name': '扩展', 'url': '', 'class': 'glyphicon glyphicon-th-list',
     'submenus': (
         {'name': '扩展', 'url': '#', 'class': 'glyphicon glyphicon-list-alt'},
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