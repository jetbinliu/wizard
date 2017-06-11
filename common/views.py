# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse('hello world')
    context = {}
    return render(request, 'common/index.html', context)