from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<cluster_type>\w+)-Cluster/$', views.index, name='dbconfig_index'),
    url(r'^add/$', views.add, name='dbconfig_add'),
    url(r'^edit/(?P<cluster_id>\d+)/$', views.edit, name="dbconfig_edit"),
    url(r'^detail/(?P<cluster_id>\d+)/$', views.detail, name="dbconfig_detail"),
    url(r'^delete/(?P<cluster_id>\d+)/$', views.delete, name="dbconfig_delete"),
    url(r'^setclusterstatus/$', views.setclusterstatus, name='setclusterstatus' ),
]