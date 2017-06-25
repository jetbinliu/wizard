# -*- coding: UTF-8 -*-

import re
import datetime


# 判断是否登录
def __is_login(request):
    return request.session.get('islogin', False)

# 验证电子邮件地址合法性，正则参考: http://tool.chinaz.com/regex/
def validateEmail(email):
    re_email = re.compile(r'^\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}$')
    if re_email.match(email):
        return True
    else:
        return False

#获取当前时间
def getNow():
    NOW = datetime.datetime.now()
    return datetime.datetime.strftime(NOW, "%Y-%m-%d %H:%M:%S")

#获取当前请求url
def _getDetailUrl(request):
    scheme = request.scheme
    host = request.META['HTTP_HOST']
    return "%s://%s/detail/" % (scheme, host)