"""
Copyright (c) Django Software Foundation and individual contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.

    3. Neither the name of Django nor the names of its contributors may be used
       to endorse or promote products derived from this software without
       specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

try:
    from django.http import JsonResponse
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder
    from django.http import HttpResponse
    from json import dumps

    class JsonResponse(HttpResponse):
        """
        An HTTP response class that consumes data to be serialized to JSON.

        :param data: Data to be dumped into json. By default only ``dict`` objects
            are allowed to be passed due to a security flaw before EcmaScript 5. See
            the ``safe`` parameter for more information.
        :param encoder: Should be an json encoder class. Defaults to
            ``django.core.serializers.json.DjangoJSONEncoder``.
        :param safe: Controls if only ``dict`` objects may be serialized. Defaults
            to ``True``.
        """

        def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
            if safe and not isinstance(data, dict):
                raise TypeError('In order to allow non-dict objects to be '
                                'serialized set the safe parameter to False')
            kwargs.setdefault('content_type', 'application/json')
            data = dumps(data, cls=encoder)
            super(JsonResponse, self).__init__(content=data, **kwargs)