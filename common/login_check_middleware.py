# -*- coding: UTF-8 -*-

import re
from django.http import HttpResponseRedirect



try:
    from django.utils.deprecation import MiddlewareMixin  # Django > 1.10.x
except ImportError:
    MiddlewareMixin = object                              # Django 1.4.x - Django 1.9.x


class LoginCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        该函数在每个函数之前检查是否登录，若未登录，则重定向到/login/
        """
        if request.session.get('login_username', False) in (False, u'匿名用户'):
            #以下是不用跳转到login页面的url白名单
            if request.path not in ('/login/', '/authenticate/') and re.match(r"/admin/\w*", request.path) is None:
                return HttpResponseRedirect('/login/')