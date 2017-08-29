from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^$', views.allworkflow, name='sqlquery_index'),
    url(r'^allworkflow/$', views.allworkflow, name='sqlquery_allworkflow'),
    url(r'^submitsql/$', views.submitsql, name='sqlquery_submitsql'),
    url(r'^autoquery/$', views.autoquery, name='sqlquery_autoquery'),
    url(r'^detail/(?P<workflowId>[0-9]+)/$', views.detail, name='sqlquery_detail'),
    url(r'^desensitization/$', views_ajax.desensitization, name='sqlquery_desensitization'),
    url(r'^getdbs/$', views_ajax.getDbsFromClusterName, name='sqlquery_getdbs'),
    url(r'gettbs/$', views_ajax.getTablesFromDb, name='sqlquery_gettbs'),
    url(r'exportcontentbydesensitization/(?P<workflowId>[0-9]+)/$', views.ExportContentByDesensitization, name='sqlquery_export'),
]