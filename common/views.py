# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # return HttpResponse('hello world')
    return render(request, 'common/login.html')