from django.conf.urls import url
from . import views, views_ajax


urlpatterns = [
    url(r'^$', views.allworkflow, name='sqlreview_index'),
    url(r'^allworkflow/$', views.allworkflow, name='sqlreview_allworkflow'),
    url(r'^simplecheck/$', views_ajax.simplecheck, name='sqlreview_simplecheck'),
    url(r'^submitsql/$', views.submitsql, name='sqlreview_submitSql'),

    url(r'^autoreview/$', views.autoreview, name='sqlreview_autoreview'),
    url(r'^detail/(?P<workflowId>[0-9]+)/$', views.detail, name='sqlreview_detail'),
    url(r'^cancel/$', views.cancel, name='sqlreview_cancel'),
    url(r'^reject/$', views.reject, name='sqlreview_reject'),
    url(r'^editsql/(?P<workflowId>[0-9]+)/$', views.editsql, name='sqlreview_editsql'),

    url(r'^execute/$', views.execute, name='sqlreview_execute'),
]