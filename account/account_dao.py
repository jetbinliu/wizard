# -*- coding:utf-8 -*-

from .models import Role, Department


# 获取角色
def getRoleById(role_id):
    role = Role.objects.values('name').get(id=role_id)
    return role['name']


def Role_Dict():
    _role_dict = Role.objects.values_list('id', 'name').all()
    role_dict = dict(_role_dict)
    return role_dict


# 获取部门
def getDepart(depart_id):
    depart = Department.objects.get(id=depart_id)
    return depart.depart_name


def Depart_Dict():
    _depart_dict = Department.objects.values_list('id', 'depart_name').all()
    depart_dict = dict(_depart_dict)
    return depart_dict


# dict
DEPART_DICT = Depart_Dict()
ROLE_DICT = Role_Dict()
