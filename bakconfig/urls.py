from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^mysqlbackup/$', views.mysql_backup, name='mysql_backup'),
]