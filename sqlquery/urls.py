from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.allworkflow, name='sqlquery_index'),
    url(r'^allworkflow/$', views.allworkflow, name='sqlquery_allworkflow'),
    url(r'submitsql/$', views.submitsql, name='sqlquery_submitsql'),
    url(r'autoquery/$', views.autoquery, name='sqlquery_autoquery'),
    url(r'^detail/(?P<workflowId>[0-9]+)/$', views.detail, name='sqlquery_detail'),
]