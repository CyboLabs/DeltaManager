from django.conf import settings


class FakseSessionCookieMiddleware(object):
    def process_request(self, request):
        ses_name = settings.SESSION_COOKIE_NAME
        if (not ses_name in request.COOKIES) \
                and request.method == 'POST' \
                and ses_name in request.POST:
            request.COOKIES[ses_name] = request.POST[ses_name]