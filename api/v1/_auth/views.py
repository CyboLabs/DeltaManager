from __future__ import absolute_import

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from .errors import RequestExists
from .utils import create_request, handle_file_upload
from ..common.errors import FileExists
from ..common.models import Device, RequestUpload
from ..common.response import JsonResponse


def _post_req_checker(request):
    if request.method != 'POST':
        res_data = {
            'result': 'failed',
            'data': {
                'message': '%s: unsupported request type.' % request.method
            }
        }
        return JsonResponse(res_data, status=405)


@csrf_exempt
def request_upload(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    device = request.POST.get('device', '')
    if not device:
        res_data['data']['message'] = 'device parameter not given'
        return JsonResponse(res_data, status=400)
    name = request.POST.get('name', '')
    if not name:
        res_data['data']['message'] = 'name parameter not given'
        return JsonResponse(res_data, status=400)

    try:
        device = int(device)
    except ValueError:
        device_q = Q(code_name=device)
    else:
        device_q = Q(id=device)
    try:
        dev_obj = Device.objects.get(device_q)
    except Device.DoesNotExist:
        res_data['data']['message'] = (
            '%s: device does not exist' % str(device)
        )
        return JsonResponse(res_data, status=404)
    except Device.MultipleObjectsReturned:
        res_data['data']['message'] = (
            '%s: multiple devices found. try using the id.'
            % str(device)
        )
        return JsonResponse(res_data, status=400)

    try:
        reference = create_request(request.user, dev_obj, name)
    except RequestExists:
        res_data['data']['message'] = (
            'A request with these parameters has already been made.'
        )
        return JsonResponse(res_data, status=403)
    except FileExists:
        res_data['data']['message'] = (
            'The file already exists'
        )
        return JsonResponse(res_data, status=403)
    res_data['result'] = 'success'
    res_data['data']['reference_id'] = reference.reference
    return JsonResponse(res_data, status=200)


@csrf_exempt
def upload(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    reference_id = request.POST.get('reference_id')
    if not reference_id:
        res_data['data']['message'] = (
            'reference_id parameter not supplied'
        )
        return JsonResponse(res_data, status=400)

    try:
        r_upload = RequestUpload.objects.get(reference=reference_id)
    except RequestUpload.DoesNotExist:
        res_data['data']['message'] = (
            '%s: reference id not valid' % reference_id
        )
        return JsonResponse(res_data, status=400)

    file = request.FILES.get('file')
    if not file:
        res_data['data']['message'] = (
            'file not included in upload'
        )
        return JsonResponse(res_data, status=400)

    _id = handle_file_upload(file, r_upload)

    res_data['status'] = 'success'
    res_data['data']['message'] = 'File uploaded'
    res_data['data']['file_id'] = int(_id)
    return JsonResponse(res_data, status=200)


@csrf_exempt
def _login(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            res_data['data']['message'] = (
                "%s: user is deactivated" % username
            )
            return JsonResponse(res_data, status=403)
    else:
        # they're unauthorised, so just return 404
        raise Http404
    res_data['result'] = 'success'
    res_data['data']['sessionid'] = request.session.session_key
    return JsonResponse(res_data, status=200)
