from __future__ import absolute_import

from django.db.models import Q
from django.http import HttpResponsePermanentRedirect
from django.views.decorators.cache import cache_page

from ..common.models import Owner, Device, File
from ..common.response import JsonResponse

default_page_size = 25


def _get_req_checker(request):
    if request.method != 'GET':
        res_data = {
            'result': 'failed',
            'data': {
                'message': '%s: unsupported request type.' % request.method
            }
        }
        return JsonResponse(res_data, status=405)


def _pk_checker(pk):
    res_data = {
        'result': 'failed',
        'data': {}
    }
    try:
        int(pk)
    except ValueError:
        res_data['data']['message'] = (
            '%s: not a valid `id` value' % pk
        )
        return JsonResponse(res_data, status=400)


@cache_page(5*60)
def file_info(request, pk):
    temp = _get_req_checker(request)
    if temp:
        return temp
    temp = _pk_checker(pk)
    if temp:
        return temp

    res_data = {
        'result': 'failed',
        'data': {}
    }

    try:
        file_obj = File.objects.get(id=int(pk))
    except File.DoesNotExist:
        res_data['data']['message'] = (
            '%s: File id does not exist' % pk
        )
        return JsonResponse(res_data, status=404)

    res_data['result'] = 'success'
    res_data['data']['file_info'] = {}
    temp = {}

    info = request.GET.get('info', None)
    if info and not info == '':
        infos = info.strip().split(',')
        for sub in infos:
            if sub == 'url':
                temp[sub] = file_obj.get_public_url()
            elif sub == 'owner':
                temp[sub] = file_obj.owner.user.username
            elif sub == 'device':
                temp[sub] = file_obj.device.code_name
            elif hasattr(file_obj, sub):
                temp[sub] = getattr(file_obj, sub)

        if not temp == {}:
            res_data['data']['file_info'] = temp
            return JsonResponse(res_data, status=200)

    res_data['data']['file_info'] = {
        'id': file_obj.id,
        'owner': file_obj.owner.user.username,
        'device': file_obj.device.code_name,
        'name': file_obj.name,
        'version': file_obj.version,
        'url': file_obj.get_public_url(),
        'size': file_obj.size,
        'download_count': file_obj.download_count,
        'md5sum': file_obj.md5sum,
        'old_version': file_obj.old_version
    }

    return JsonResponse(res_data, status=200)


def download(request, pk):
    temp = _get_req_checker(request)
    if temp:
        return temp
    temp = _pk_checker(pk)
    if temp:
        return temp

    res_data = {
        'result': 'failed',
        'data': {}
    }

    try:
        file_obj = File.objects.get(id=int(pk))
    except File.DoesNotExist:
        res_data['data']['message'] = (
            '%s: File id does not exist' % pk
        )
        return JsonResponse(res_data, status=404)

    file_obj.download_count += 1
    file_obj.save()
    return HttpResponsePermanentRedirect(file_obj.get_direct_url())


def _calc_page_size(request):
    size = request.GET.get('size', default_page_size)
    if not isinstance(size, int):
        size = default_page_size
    elif size > 100:
        size = 100
    start = request.GET.get('start', 0)
    if not isinstance(start, int):
        start = 0
    return start, size


def list_files(request):
    temp = _get_req_checker(request)
    if temp:
        return temp

    res_data = {
        'result': 'failed',
        'data': {}
    }

    device = request.GET.get('device', '')
    device_q = Q(device__code_name=device) if device else Q()

    owner = request.GET.get('owner', '')
    owner_q = Q(user__username=owner) if owner else Q()

    start, size = _calc_page_size(request)

    model_list = File.objects.filter(
        device_q, owner_q
    )[start:start+size]
    if not model_list:
        res_data['data']['message'] = 'no files to show'
        return JsonResponse(res_data, status=404)

    data = []
    for _id, name in model_list.values_list('id', 'name'):
        data.append({'id': _id, 'name': name})

    res_data['result'] = 'success'
    res_data['data']['file_list'] = data
    return JsonResponse(res_data, status=200)


def list_devices(request):
    temp = _get_req_checker(request)
    if temp:
        return temp

    res_data = {
        'result': 'failed',
        'data': {}
    }

    start, size = _calc_page_size(request)

    model_list = Device.objects.all()[start:start+size]
    if not model_list:
        res_data['data']['message'] = 'no devices to show'
        return JsonResponse(res_data, status=404)

    data = []
    for _id, code_name in model_list.values_list('id', 'code_name'):
        data.append({'id': _id, 'name': code_name})

    res_data['result'] = 'success'
    res_data['data']['device_list'] = data
    return JsonResponse(res_data, status=200)


def list_owners(request):
    temp = _get_req_checker(request)
    if temp:
        return temp

    res_data = {
        'result': 'failed',
        'data': {}
    }

    start, size = _calc_page_size(request)

    model_list = Owner.objects.all()[start:start+size]
    if not model_list:
        res_data['data']['message'] = 'no owners to show'
        return JsonResponse(res_data, status=404)

    data = []
    for _id, name in model_list.values_list('id', 'user__username'):
        data.append({'id': _id, 'username': name})

    res_data['result'] = 'success'
    res_data['data']['file_list'] = data
    return JsonResponse(res_data, status=200)