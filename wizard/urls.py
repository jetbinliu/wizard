"""wizard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
# from django.contrib import admin
from common import views as common_views
from account import views as account_views, views_ajax as account_views_ajax

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', common_views.index, name='index'),
    url(r'^index/$', common_views.index, name='index'),
    url(r'^login/$', account_views.login, name='login'),
    url(r'^logout/$', account_views.logout, name='logout'),
    url(r'^authenticate/$', account_views_ajax.authenticate),
    url(r'^account/', include('account.urls')),
    url(r'^common/', include('common.urls')),
]
