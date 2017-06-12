from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.allworkflow, name='sqlreview_index'),
    url(r'^allworkflow/$', views.allworkflow, name='sqlreview_allworkflow'),
    url(r'^submitsql/$', views.submitsql, name='sqlreview_submitSql'),
]