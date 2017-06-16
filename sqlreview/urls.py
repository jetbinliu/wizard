from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^$', views.allworkflow, name='sqlreview_index'),
    url(r'^allworkflow/$', views.allworkflow, name='sqlreview_allworkflow'),
    url(r'^submitsql/$', views.submitsql, name='sqlreview_submitSql'),
    url(r'^simplecheck/$', views_ajax.simplecheck, name='simplecheck'),

    url(r'^autoreview/$', views.autoreview, name='autoreview'),
    url(r'^detail/(?P<workflowId>[0-9]+)/$', views.detail, name='detail'),
]