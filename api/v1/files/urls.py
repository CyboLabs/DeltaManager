from __future__ import absolute_import

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^file_list/', views.list_files),
                       url(r'^owner_list/', views.list_owners),
                       url(r'^device_list/', views.list_devices),
                       url(r'^file_info/(?P<pk>[0-9]+)/', views.file_info),
                       url(r'^download/(?P<pk>[0-9]+)/.*', views.download),
                       )