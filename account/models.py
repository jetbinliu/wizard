# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#角色分3种：
#1.开发人员：可以提交SQL上线单的工程师们，username字段为登录用户名，realname字段为展示的中文名。
#2.审核人：可以审核并执行SQL上线单的管理员、DBA、超级管理员们。
#3.普通用户

# 超级管理员
# 管理员
# dba
# leader
# 项目管理
# 开发人员
# 普通用户

class Users(AbstractUser):
    # 真实姓名
    realname = models.CharField(max_length=32)
    # 电话
    phone = models.CharField(max_length=15, blank=True)
    # 部门
    department = models.IntegerField(blank=True,default=1)
    # 角色
    role = models.IntegerField(blank=True,default=5)

class Department(models.Model):
    # 部门名称
    depart_name = models.CharField(max_length=50, blank=True)

# 角色　角色只是相当于权限的一个集合,能够方便快捷的为用户分配权限   参看　auth_group
class Role(models.Model):
    #主键由Django生成
    name = models.CharField(max_length=64) # 角色名称
    code = models.CharField(max_length=32) # 角色code
    desc = models.CharField(max_length=255) # 角色描述