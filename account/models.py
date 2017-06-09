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
    role = models.CharField('角色', max_length=20, choices=(('工程师','工程师'),('审核人','审核人'),('副审核人','副审核人')), default='工程师')

class Department(models.Model):
    # 部门名称
    depart_name = models.CharField(max_length=50, blank=True)
