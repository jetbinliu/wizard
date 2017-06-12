# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import cluster_config

# Create your views here.
# 显示用户列表
def index(request):
    clusters = cluster_config.objects.all()
    context = {
        'clusters': clusters,
        'currentMenu': 'dbconfig',
    }
    return render(request, 'dbconfig/index.html', context)


def add(request):
    if request.POST:
        cluster_type = request.POST.get("cluster_type")
        cluster_name = request.POST.get("cluster_name")
        cluster_hosts = request.POST.get("cluster_hosts")
        cluster_port = request.POST.get("cluster_port")
        cluster_user = request.POST.get("cluster_user")
        cluster_password = request.POST.get("cluster_password")
        # 验证重复的帐号名
        cluster_name = cluster_config.objects.filter(clustername__iexact=cluster_name)
        # 验证重复的邮件地址
        cluster_port = cluster_config.objects.filter(email__iexact=cluster_port)
        if cluster_name:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'集群名称已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        if cluster_port:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'集群端口已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')

        # 保存用户信息
        # 密码由用户名单向散列得到,如果登录时使用LADP 验证真正的用户名和密码

        clusters = cluster_config(
            cluster_type=cluster_type,
            cluster_name=cluster_name,
            cluster_hosts=cluster_hosts,
            cluster_port=cluster_port,
            cluster_user=cluster_user,
            cluster_password=cluster_password)
        clusters.save()

        return HttpResponseRedirect("/dbconfig/index")

    context = {}
    return render(request, 'dbconfig/add.html', context)


def edit(request, cluster_id):
    cluster = cluster_config.objects.get(id=int(cluster_id))
    if not cluster:
        return HttpResponseBadRequest(u"错误请求")
    if request.POST:
        cluster_type = request.POST.get("cluster_type")
        cluster_name = request.POST.get("cluster_name")
        cluster_hosts = request.POST.get("cluster_hosts")
        cluster_port = request.POST.get("cluster_port")
        cluster_user = request.POST.get("cluster_user")
        cluster_password = request.POST.get("cluster_password")
        cluster.save()
        return HttpResponseRedirect("/dbconfig/index")
    context = {'cluster': cluster}
    return render(request, 'dbconfig/edit.html', context)

def detail(request, cluster_id):
    cluster = cluster_config.objects.get(id=int(cluster_id))
    if not cluster:
        return HttpResponseRedirect("/dbconfig/index")
    context = {'cluster': cluster}
    return render(request, 'dbconfig/detail.html', context)

def delete(request, cluster_id):
    cluster = None
    try:
        cluster = cluster_config.objects.get(id = int(cluster_id))
    except BaseException:
        return HttpResponse(json.dumps({"statusCode":400,"message":u'此用户不存在!'}), content_type='application/json')
    # 删除此用户
    cluster.delete()
    return HttpResponseRedirect("/dbconfig/index")
