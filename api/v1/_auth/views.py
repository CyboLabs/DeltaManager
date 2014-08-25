from __future__ import absolute_import

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt

from .errors import RequestExists
from .utils import create_request, handle_file_upload
from ..common.errors import FileExists, UserExists, OwnerExists, ManufacturerExists, DeviceExists
from ..common.models import Device, RequestUpload, Manufacturer
from ..common.response import JsonResponse
from ..common.utils import create_user_owner, create_manufacturer, create_device


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


def _logout(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    logout(request)

    res_data = {
        'result': 'success',
        'data': {
            'message': 'Logout successful'
        }
    }
    return JsonResponse(res_data, status=200)


def view_create_user(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    if not request.user.is_staff:
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    username = request.POST.get('username')
    if not username:
        res_data['data']['message'] = "username parameter not supplied"
        return JsonResponse(res_data, status=400)
    password = request.POST.get('password')
    if not password:
        res_data['data']['message'] = "password parameter not supplied"
        return JsonResponse(res_data, status=400)

    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')

    is_staff = bool(request.POST.get('is_staff', False))
    is_super = bool(request.POST.get('is_super', False))
    if not request.user.is_superuser and (
            is_staff or is_super):
        res_data['data']['message'] = (
            "You are not authorised to give people raised rights")
        return JsonResponse(res_data, status=403)

    try:
        user, owner = create_user_owner(username, password,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        is_staff=is_staff,
                                        is_super=is_super)
    except UserExists:
        res_data['data']['message'] = (
            'user already exists'
        )
        return JsonResponse(res_data, status=400)
    except OwnerExists:
        res_data['data']['message'] = (
            'owner already exists'
        )
        return JsonResponse(res_data, status=400)

    res_data['result'] = 'success'
    res_data['data']['message'] = 'User successfully created'
    res_data['data']['owner_id'] = owner.id
    res_data['data']['username'] = user.username
    return JsonResponse(res_data, status=200)


def view_create_manufacturer(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    if not request.user.is_staff:
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    code_name = request.POST.get('code_name')
    if not code_name:
        res_data['data']['message'] = "code_name parameter not supplied"
        return JsonResponse(res_data, status=400)
    full_name = request.POST.get('full_name')
    if not full_name:
        res_data['data']['message'] = "full_name parameter not supplied"
        return JsonResponse(res_data, status=400)

    try:
        manu = create_manufacturer(code_name, full_name)
    except ManufacturerExists:
        res_data['data']['message'] = (
            'manufacturer exists already'
        )
        return JsonResponse(res_data, status=400)

    res_data['result'] = 'success'
    res_data['data']['message'] = 'manufacturer successfully created'
    res_data['data']['manufacturer_id'] = manu.id
    return JsonResponse(res_data, status=200)


def view_create_device(request):
    temp = _post_req_checker(request)
    if temp:
        raise Http404

    if not request.user.is_authenticated():
        raise Http404

    if not request.user.is_staff:
        raise Http404

    res_data = {
        'result': 'failed',
        'data': {}
    }

    code_name = request.POST.get('code_name')
    if not code_name:
        res_data['data']['message'] = "code_name parameter not supplied"
        return JsonResponse(res_data, status=400)
    full_name = request.POST.get('full_name')
    if not full_name:
        res_data['data']['message'] = "full_name parameter not supplied"
        return JsonResponse(res_data, status=400)
    manufacturer = request.POST.get('manufacturer')
    if not manufacturer:
        res_data['data']['message'] = "manufacturer parameter not supplied"
        return JsonResponse(res_data, status=400)

    try:
        manufacturer = int(manufacturer)
    except ValueError:
        manu_q = Q(code_name=manufacturer)
    else:
        manu_q = Q(id=manufacturer)
    try:
        manu_obj = Manufacturer.objects.get(manu_q)
    except Manufacturer.DoesNotExist:
        res_data['data']['message'] = (
            '%s: manufacturer does not exist' % str(manufacturer)
        )
        return JsonResponse(res_data, status=404)
    except Manufacturer.MultipleObjectsReturned:
        res_data['data']['message'] = (
            '%s: multiple manufacturers found. try using the id.'
            % str(manufacturer)
        )
        return JsonResponse(res_data, status=400)

    try:
        device = create_device(code_name, full_name, manu_obj)
    except DeviceExists:
        res_data['data']['message'] = (
            'device exists already'
        )
        return JsonResponse(res_data, status=400)

    res_data['result'] = 'success'
    res_data['data']['message'] = 'device successfully created'
    res_data['data']['device_id'] = device.id
    return JsonResponse(res_data, status=200)