from __future__ import absolute_import

from django.contrib.auth.models import User

from .errors import (UserExists, OwnerExists, ManufacturerExists,
                     DeviceExists, FileExists)
from .models import Owner, Device, File, Manufacturer

from hashlib import md5


def make_md5sum(filename, bs=524288):
    """efficiently get md5 of file

    The `blocksize` should be set to the most optimal value.
    512k gave the best results (1.826s vs 2.513s for 5 runs)
    """
    hasher = md5()
    with open(filename, 'rb') as f:
        buf = f.read(bs)
        while buf:
            hasher.update(buf)
            buf = f.read(bs)
    return hasher.hexdigest()


def create_user(username, password, first_name="", last_name="",
                email="", is_staff=False):

    try:
        User.objects.get(username__exact=username)
    except User.DoesNotExist:
        pass
    else:
        raise UserExists(username)

    user = User.objects.create_user(username,
                                    password=password,
                                    first_name=first_name,
                                    last_name=last_name,
                                    email=email)
    if is_staff:
        user.is_staff = True
        user.is_superuser = True
    user.save()

    return user


def create_owner(user):
    try:
        Owner.objects.get(user=user)
    except Owner.DoesNotExist:
        pass
    else:
        raise OwnerExists(user.username)
    return Owner.objects.create(user=user)


def create_user_owner(username, password, first_name='', last_name='',
                      email='', is_staff=False):
    user = create_user(username, password, first_name, last_name,
                       email, is_staff)
    owner = create_owner(user)
    return user, owner


def create_manufacturer(code_name, full_name):
    try:
        Manufacturer.objects.get(code_name=code_name)
        Manufacturer.objects.get(full_name=full_name)
    except Manufacturer.DoesNotExist:
        pass
    else:
        raise ManufacturerExists(code_name)
    return Manufacturer.objects.create(code_name=code_name,
                                       full_name=full_name)


def create_device(code_name, full_name, manufacturer):
    try:
        Device.objects.get(code_name=code_name,
                           manufacturer=manufacturer)
    except Device.DoesNotExist:
        pass
    else:
        raise DeviceExists((code_name, manufacturer.code_name))
    return Device.objects.create(code_name=code_name,
                                 full_name=full_name,
                                 manufacturer=manufacturer)


def create_manu_device(manu_code_name, manu_full_name,
                       device_code_name, device_full_name):
    manu = create_manufacturer(manu_code_name, manu_full_name)
    device = create_device(device_code_name, device_full_name, manu)
    return manu, device


def create_file(owner, device, name, size, md5sum,
                version='', old_version=''):
    try:
        File.objects.get(owner=owner,
                         device=device,
                         name=name)
    except File.DoesNotExist:
        pass
    else:
        raise FileExists((owner, device, name))
    return File.objects.create(owner=owner,
                               device=device,
                               name=name,
                               version=version,
                               size=size,
                               md5sum=md5sum,
                               old_version=old_version)