from __future__ import absolute_import

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^login/', views._login),
                       url(r'^logout/', views._logout),
                       url(r'^request_upload/', views.request_upload),
                       url(r'^upload/', views.upload),
                       url(r'^create_user/', views.view_create_device),
                       url(r'^create_manufacturer/', views.view_create_manufacturer),
                       url(r'^create_device/', views.view_create_device),
                       )