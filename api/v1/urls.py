from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from .files import urls as files_urls
from ._auth import urls as auth_urls
from .common.response import JsonResponse

urlpatterns = patterns('',
                       url(r'^auth/', include(auth_urls)),
                       url(r'^files/', include(files_urls)),
                       )