from __future__ import absolute_import

from ..common.errors import BaseExists


class RequestExists(BaseExists):
    msg = 'Request for file exists already'