# -*- coding: UTF-8 -*-
import json
import re

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q

from .models import mysql_cluster_config, redis_cluster_config, mongodb_cluster_config, CLUSTER_ROLE, CLUSTER_STATUS
from .dbconfigDal import setClusterStatusByHostPort
from common.aes_decryptor import Prpcrypt

# Create your views here.
# 显示用户列表
def index(request, cluster_type = "MySQL"):
    _cluster_type = cluster_type.lower()
    if _cluster_type == 'mysql':
        _dao = mysql_cluster_config
    elif _cluster_type == 'redis':
        _dao = redis_cluster_config
    elif _cluster_type == 'mongodb':
        _dao = mongodb_cluster_config
    else:
        return HttpResponse(status=403)

    clusters = _dao.objects.all()
    for cluster in clusters:
        cluster.cluster_role = CLUSTER_ROLE.get(cluster.cluster_role)
    context = {
        'cluster_type': cluster_type,
        'clusters': clusters,
    }
    return render(request, 'dbconfig/index.html', context)


def add(request):
    if request.POST:
        pathname = request.POST.get("pathname")
        cluster_name = request.POST.get("cluster_name")
        cluster_role = int(request.POST.get("cluster_role"))
        cluster_host = request.POST.get("cluster_host")
        cluster_port = int(request.POST.get("cluster_port"))
        cluster_user = request.POST.get("cluster_user")
        cluster_password = request.POST.get("cluster_password")

        cluster_type = re.split(r'\W+', pathname)[2]
        _cluster_type = cluster_type.lower()
        if _cluster_type == 'mysql':
            _dao = mysql_cluster_config
        elif _cluster_type == 'redis':
            _dao = redis_cluster_config
        elif _cluster_type == 'mongodb':
            _dao = mongodb_cluster_config
        else:
            return HttpResponse(status=403)

        # 验证重复的主库
        cluster_masters = _dao.objects.filter(Q(cluster_name__iexact=cluster_name) & Q(cluster_role__exact=1))
        if cluster_masters and cluster_role == 1:
            context = {'errMsg': u'集群主库已经存在不能添加！'}
            return render(request, 'error.html', context)

        # 保存用户信息
        cluster = _dao(
            cluster_name=cluster_name,
            cluster_role=cluster_role,
            cluster_host=cluster_host,
            cluster_port=cluster_port,
            cluster_user=cluster_user,
            cluster_password=cluster_password)
        cluster.save()

        return HttpResponseRedirect(pathname)

    context = {'CLUSTER_ROLE':CLUSTER_ROLE}
    return render(request, 'dbconfig/add.html', context)


def edit(request, cluster_id):
    HTTP_REFERER = request.META.get("HTTP_REFERER")
    cluster_type = re.split(r'\W+', HTTP_REFERER)[-3]
    _cluster_type = cluster_type.lower()
    if _cluster_type == 'mysql':
        _dao = mysql_cluster_config
    elif _cluster_type == 'redis':
        _dao = redis_cluster_config
    elif _cluster_type == 'mongodb':
        _dao = mongodb_cluster_config
    else:
        return HttpResponse(status=403)

    cluster = _dao.objects.get(id=int(cluster_id))
    if not cluster:
        context = {'errMsg': u'错误请求！'}
        return render(request, 'error.html', context)

    if request.POST:
        cluster.id = int(request.POST.get("cluster_id"))
        cluster.cluster_name = request.POST.get("cluster_name")
        cluster.cluster_role = int(request.POST.get("cluster_role"))
        cluster.cluster_host = request.POST.get("cluster_host")
        cluster.cluster_port = int(request.POST.get("cluster_port"))
        cluster.cluster_user = request.POST.get("cluster_user")
        cluster.cluster_password = request.POST.get("cluster_password")
        cluster.cluster_status = request.POST.get("cluster_status")

        # 验证重复的主库
        cluster_masters = _dao.objects.filter(Q(cluster_name__iexact=cluster.cluster_name) & Q(cluster_role__exact=1))
        if cluster_masters and cluster.cluster_role == 1:
            # 排除修改主库本身
            if cluster.id not in [cluster_master.id for cluster_master in cluster_masters]:
                context = {'errMsg': u'集群主库已经存在不能添加！'}
                return render(request, 'error.html', context)
        cluster.save()
        return HttpResponseRedirect(HTTP_REFERER)

    pc = Prpcrypt()  # 初始化
    cluster.cluster_password = pc.decrypt(cluster.cluster_password)
    context = {'cluster':cluster, 'CLUSTER_ROLE':CLUSTER_ROLE, 'CLUSTER_STATUS':CLUSTER_STATUS}
    return render(request, 'dbconfig/edit.html', context)


def detail(request, cluster_id):
    HTTP_REFERER = request.META.get("HTTP_REFERER")
    cluster_type = re.split(r'\W+', HTTP_REFERER)[-3]
    _cluster_type = cluster_type.lower()
    if _cluster_type == 'mysql':
        _dao = mysql_cluster_config
    elif _cluster_type == 'redis':
        _dao = redis_cluster_config
    elif _cluster_type == 'mongodb':
        _dao = mongodb_cluster_config
    else:
        return HttpResponse(status=403)

    cluster = _dao.objects.get(id=int(cluster_id))
    if cluster:
        cluster.cluster_role = CLUSTER_ROLE.get(cluster.cluster_role)
    else:
        return HttpResponseRedirect(HTTP_REFERER)

    context = {'cluster':cluster}
    return render(request, 'dbconfig/detail.html', context)


def delete(request, cluster_id):
    HTTP_REFERER = request.META.get("HTTP_REFERER")
    cluster_type = re.split(r'\W+', HTTP_REFERER)[-3]
    _cluster_type = cluster_type.lower()
    if _cluster_type == 'mysql':
        _dao = mysql_cluster_config
    elif _cluster_type == 'redis':
        _dao = redis_cluster_config
    elif _cluster_type == 'mongodb':
        _dao = mongodb_cluster_config
    else:
        return HttpResponse(status=403)

    try:
        cluster = _dao.objects.get(id = int(cluster_id))
    except BaseException:
        context = {'errMsg': u'此用户不存在！'}
        return render(request, 'error.html', context)
    # 删除此用户
    cluster.delete()
    return HttpResponseRedirect(HTTP_REFERER)

@csrf_exempt
def setclusterstatus(request):
    cluster_type = request.POST.get("cluster_type")
    host = request.POST.get("host")
    port = request.POST.get("port")
    stat = request.POST.get("stat")
    rets = setClusterStatusByHostPort(cluster_type,host,port,stat)
    return HttpResponse(json.dumps(rets), content_type='application/json')
