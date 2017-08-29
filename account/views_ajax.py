# -*- coding: UTF-8 -*-

import json
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt

from .models import Users
from lib.util import getNow

@csrf_exempt
def authenticate(request):
    if request.is_ajax():
        strUsername = request.POST.get("username")
        strPassword = request.POST.get("password")
    else:
        strUsername = request.POST['username']
        strPassword = request.POST['password']

    result = {}
    # 服务端二次验证参数
    if not strUsername:
        result = {'status':2, 'msg':'登录用户名为空，请重新输入!', 'data':''}
        return HttpResponse(json.dumps(result), content_type='application/json')
    if not strPassword:
        result = {'status': 2, 'msg': '登录密码为空，请重新输入!', 'data': ''}
        return HttpResponse(json.dumps(result), content_type='application/json')

    correct_users = Users.objects.filter(username=strUsername)
    # 调用了django内置函数check_password函数检测输入的密码是否与django默认的PBKDF2算法相匹配
    if len(correct_users) == 1:
        if check_password(strPassword, correct_users[0].password):
            correct_users[0].last_login = getNow()
            correct_users[0].save()
            request.session['login_username'] = strUsername
            result = {'status':0, 'msg':'ok', 'data':''}
        else:
            result = {'status':1, 'msg':'密码错误，请重新输入！', 'data':''}
    else:
        result = {'status': 2, 'msg': '登录用户不存在，请重新输入！', 'data': ''}
    return HttpResponse(json.dumps(result), content_type='application/json')