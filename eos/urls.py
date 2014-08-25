from django.conf.urls import patterns, include, url

from api.v1.common.response import JsonResponse

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eos.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('api.v1.urls')),
)


def handler400(request):
    res_data = {
        'result': 'failed',
        'data': {
            'message': 'Bad Request (400)'
        }
    }
    return JsonResponse(res_data, status=400)


def handler403(request):
    res_data = {
        'result': 'failed',
        'data': {
            'message': 'Permission Denied (403)'
        }
    }
    return JsonResponse(res_data, status=403)


def handler404(request):
    res_data = {
        'result': 'failed',
        'data': {
            'message': 'Page Not Found (404)'
        }
    }
    return JsonResponse(res_data, status=404)


def handler500(request):
    res_data = {
        'result': 'failed',
        'data': {
            'message': 'Server Error (500)'
        }
    }
    return JsonResponse(res_data, status=500)