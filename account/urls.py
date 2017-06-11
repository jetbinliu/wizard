from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='account_index'),
    url(r'^index/$', views.index, name='account_index'),
    url(r'^add/$', views.add, name='account_add'),
    url(r'^edit/(?P<user_id>\d+)/$', views.edit,name="account_edit"),
    url(r'^detail/(?P<user_id>\d+)/$', views.detail, name="account_detail"),
    url(r'^delete/(?P<user_id>\d+)/$', views.delete, name="account_delete"),
]