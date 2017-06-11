# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
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