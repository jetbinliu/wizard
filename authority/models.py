# -*- coding: UTF-8 -*-

import json

from django.db import models
from django.contrib.auth.decorators import PermissionDenied, user_passes_test

from account.models import Users

# Create your models here.
# 权限 每一个权限控制点在此表中表现为一条记录 参看auth_permission
class Permission(models.Model):
    codename = models.CharField(max_length=64, unique=True)  # codename 用于控制
    desc = models.CharField(max_length=255)  # 描述
    # 类型 1:用户和角色 2:应用项　相关权限 3:监控项　相关权限 4:树状节点 相关权限
    type = models.IntegerField()  # 1:'系统管理', 2:'配置管理', 3:'工作台', 4:'区域工单管理', 5:'字段展现', 6:'其他'

    # 用户
    users = models.ManyToManyField(Users)  # 用户与权限多对多关联

    # 重新定义表名
    class Meta:
        db_table = 'permission'
        # unique_together = ('codename',)


# 装饰标记@permission_required
# 表示用户是否拥有特定权限，访问某个view权限，
# 验证失败,则重定向到login_url
# 如果raise_exception 参数为True,验证失败会抛出异常
def permission_required(perm, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if neccesary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        # First check if the user has the permission (even anon users)
        if user.has_perm(perm):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)