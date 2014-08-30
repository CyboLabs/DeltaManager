from __future__ import absolute_import

from .errors import RequestExists
from ..common.errors import FileExists
from ..common.models import File, Owner, RequestUpload
from ..common.utils import create_file

from eos.settings import DOWNLOAD_STORAGE

from errno import EEXIST
from hashlib import md5
from os import path, makedirs
from random import choice
from string import ascii_letters, digits


def create_request(user, device, name, old_version='', version=''):
    owner = Owner.objects.get(user=user)
    try:
        RequestUpload.objects.get(owner=owner, device=device, name=name)
    except RequestUpload.DoesNotExist:
        pass
    else:
        raise RequestExists((user.username, device.code_name, name))
    try:
        File.objects.get(owner=owner, device=device, name=name)
    except File.DoesNotExist:
        pass
    else:
        raise FileExists((user.username, device.code_name, name))

    reference = ''.join(choice(ascii_letters + digits) for _ in range(32))
    return RequestUpload.objects.create(owner=owner,
                                        device=device,
                                        name=name,
                                        version=version,
                                        old_version=old_version,
                                        reference=reference)


def create_dir_tree(location):
    _dir = path.dirname(location)
    try:
        makedirs(_dir)
    except OSError as e:
        if e.errno == EEXIST and path.isdir(_dir):
            pass
        else:
            raise Exception("%s: Can't make directory"
                            % _dir)


def handle_file_upload(f, r_upload):
    hasher = md5()
    size = f.size
    location = DOWNLOAD_STORAGE % {
        'name': r_upload.name,
        'owner': r_upload.owner.user.username,
        'device': r_upload.device.code_name
    }

    create_dir_tree(location)
    with open(location, 'wb+') as destination:
        for chunk in f.chunks():
            hasher.update(chunk)
            destination.write(chunk)

    file = create_file(r_upload.owner, r_upload.device,
                       r_upload.name, size, hasher.hexdigest(),
                       version=r_upload.version,
                       old_version=r_upload.old_version)
    r_upload.delete()
    return file.id