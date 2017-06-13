# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.hashers import make_password
# from django.utils import simplejson

from .models import Users
from .account_dao import DEPART_DICT, ROLE_DICT

# Create your views here.
# 用户登录
def login(request):
    return render(request, 'account/login.html')

def logout(request):
    if request.session.get('login_username'):
        del request.session['login_username']
    return render(request, 'account/login.html')

def authenticate(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        request.session['login_username'] = username
        return HttpResponseRedirect('/index/')
    else:
        return HttpResponse('haha')

# 显示用户列表
def index(request):
    users = Users.objects.all()
    for user in users:
        user.role = ROLE_DICT.get(user.role)
        user.department = DEPART_DICT.get(user.department)
    context = {
        'users': users,
        'currentMenu': 'userconfig',
    }
    return render(request, 'account/index.html', context)


def add(request):
    if request.POST:
        username = request.POST.get("username")
        realname = request.POST.get("realname")
        email = request.POST.get("email")
        role = request.POST.get("role")
        department = request.POST.get("department")
        phone = request.POST.get("phone")
        # 验证重复的帐号名
        usernames = Users.objects.filter(username__iexact=username)
        # 验证重复的邮件地址
        emails = Users.objects.filter(email__iexact=email)
        if usernames:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'用户名已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        if emails:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'邮件地址已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')

        # 保存用户信息
        # 密码由用户名单向散列得到,如果登录时使用LADP 验证真正的用户名和密码
        password = make_password(username, salt=None, hasher='default')
        user = Users(username=username, email=email, password=password,
                     role=role, department=department, phone=phone, realname=realname)
        user.save()

        return HttpResponseRedirect("/account/index")

    context = {'DEPART_DICT': DEPART_DICT, 'ROLE_DICT': ROLE_DICT}
    return render(request, 'account/add.html', context)


def edit(request, user_id):
    user = Users.objects.get(id=int(user_id))
    if not user:
        return HttpResponseBadRequest(u"错误请求")
    if request.POST:
        user.department = request.POST.get("department")
        user.realname = request.POST.get("realname")
        user.phone = request.POST.get("phone")
        user.role = request.POST.get("role")
        user.save()
        return HttpResponseRedirect("/account/index")
    context = {'user': user, 'ROLE_DICT': ROLE_DICT, 'DEPART_DICT': DEPART_DICT}
    return render(request, 'account/edit.html', context)

def detail(request, user_id):
    user = Users.objects.get(id=int(user_id))
    if not user:
        return HttpResponseRedirect("/account/index")
    context = {'user': user, 'ROLE_DICT': ROLE_DICT, 'DEPART_DICT': DEPART_DICT}
    return render(request, 'account/detail.html', context)

def delete(request, user_id):
    user = None
    try:
        user = Users.objects.get(id = int(user_id))
    except BaseException:
        return HttpResponse(json.dumps({"statusCode":400,"message":u'此用户不存在!'}), content_type='application/json')
    # 删除此用户
    user.delete()
    return HttpResponseRedirect("/account/index")

