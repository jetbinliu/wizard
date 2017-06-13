# -*- coding: UTF-8 -*-


from django.shortcuts import render

from dbconfig.models import cluster_config

# Create your views here.
def allworkflow(request):
    return render(request, 'sqlreview/allworkflow.html')

# 提交SQL的页面
def submitsql(request):
    clusters = cluster_config.objects.filter(cluster_type=1)
    if len(clusters) == 0:
       context = {'errMsg': '集群数为0，可能后端数据没有配置集群'}
       return render(request, 'error.html', context)

    return render(request, 'sqlreview/submitsql.html')
