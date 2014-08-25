from __future__ import absolute_import

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^login/', views._login),
                       url(r'^request_upload/', views.request_upload),
                       url(r'^upload/', views.upload)
                       )