from django.shortcuts import render

# Create your views here.
def allworkflow(request):
    return render(request, 'sqlreview/allworkflow.html')

# 提交SQL的页面
def submitsql(request):
    return render(request, 'sqlreview/submitsql.html')
