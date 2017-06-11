# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
# from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from .models import Users

def authenticate(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    correct_users = Users.objects.filter(username=username)
    if len(correct_users) == 1 and check_password(password, correct_users[0].password) == True:
        request.session['login_username'] = username
        return HttpResponseRedirect('/index/')
    else:
        return HttpResponse('haha')