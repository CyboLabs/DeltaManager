from __future__ import absolute_import, print_function

from django.db.models import Q
from django.core.files import File as DJFile

from api.v1._auth.utils import *
from api.v1.common.utils import *
from api.v1.common.errors import *
from api.v1.common.models import *

from getpass import getpass
from tempfile import mkstemp
from os import close as os_close, remove


def get_device(_id=None, code_name=None, full_name=None):
    q_id = Q(id=_id) if _id else Q()
    q_cn = Q(code_name=code_name) if code_name else Q()
    q_fn = Q(full_name=full_name) if full_name else Q()

    # I'm a lumberjack and I don't care
    # let them filter the exceptions
    return Device.objects.get(q_id, q_cn, q_fn)


def get_user(_id=None, username=None):
    q_id = Q(id=_id) if _id else Q()
    q_un = Q(username=username) if username else Q()

    return User.objects.get(q_id, q_un)


def get_owner(_id=None, username=None):
    q_id = Q(id=_id) if _id else Q()
    q_un = Q(user__username=username) if username else Q()

    return Owner.objects.get(q_id, q_un)


def get_manu(_id=None, code_name=None, full_name=None):
    q_id = Q(id=_id) if _id else Q()
    q_cn = Q(code_name=code_name) if code_name else Q()
    q_fn = Q(full_name=full_name) if full_name else Q()

    return Manufacturer.objects.get(q_id, q_cn, q_fn)


# (code_name, full_name)
manu_list = [
    ('htc', 'HTC'),
    ('lge', 'LG Electronics'),
    ('sony', 'Sony'),
    ('samsung', 'Samsung'),
    ('motorola', 'Motorola'),
    ('oppo', 'Oppo'),
    ('op', 'OnePlus'),
    ('asus', 'ASUS'),
    ('hp', 'HP')
]


# (code_name, full_name, manufacturer__code_name)
device_list = [
    ('bacon', 'One', 'op'),
    ('d800', 'G2 AT&T', 'lge'),
    ('d801', 'G2 T-Mobile', 'lge'),
    ('d802', 'G2 Europe', 'lge'),
    ('d803', 'G2 Canada', 'lge'),
    ('deb', 'Nexus 7 (2013) LTE', 'asus'),
    ('dlx', 'DROID DNA', 'htc'),
    ('everest', 'Xoom 3g', 'motorola'),
    ('evita', 'One Xl', 'htc'),
    ('f320', 'G2 Korea', 'lge'),
    ('falcon', 'Moto G', 'motorola'),
    ('find5', 'Find 5', 'oppo'),
    ('find7', 'Find 7', 'oppo'),
    ('find7a', 'Find 7a', 'oppo'),
    ('fireball', 'Incredible 4G', 'htc'),
    ('flo', 'Nexus 7 (2013', 'asus'),
    ('grouper', 'Nexus 7', 'asus'),
    ('hammerhead', 'Nexus 5', 'lge'),
    ('jewel', 'Evo 4g', 'htc'),
    ('ls980', 'G2 Sprint', 'lge'),
    ('m7', 'One M7', 'htc'),
    ('m7spr', 'One M7 Sprint', 'htc'),
    ('m7vzw', 'One M7 Verizon', 'htc'),
    ('m8', 'One M8', 'htc'),
    ('maguro', 'Galaxy Nexus', 'samsung'),
    ('mako', 'Nexus 4', 'lge'),
    ('manta', 'Nexus 10', 'samsung'),
    ('n1', 'N1', 'oppo'),
    ('stingray', 'Xoom Verizon', 'motorola'),
    ('stingray_cdma', 'Xoom CDMA', 'motorola'),
    ('tenderloin', 'Touchpad', 'hp'),
    ('tilapia', 'Nexus 7 3g', 'asus'),
    ('toro', 'Galaxy Nexus', 'samsung'),
    ('toroplus', 'Galaxy Nexus', 'samsung'),
    ('ville', 'One S', 'htc'),
    ('vs980', 'G2 Verizon', 'lge'),
    ('wingray', 'Xoom', 'motorola'),
]

# (username, password, first_name, last_name, email, is_staff, is_super)
user_list = [
    ('eos', None, '', '', '', True, False)
]

# user__username
owner_list = [
    'eos'
]


file_name = '%(device)s-blah%(num)s'


def create_manu_base():
    for code_name, full_name in manu_list:
        try:
            create_manufacturer(code_name, full_name)
        except ManufacturerExists:
            pass


def create_device_base():
    for code_name, full_name, manu_name in device_list:
        manu = get_manu(code_name=manu_name)
        try:
            create_device(code_name, full_name, manu)
        except DeviceExists:
            pass


def create_user_base():
    for username, password, first_name, \
            last_name, email, is_staff, is_super in user_list:
        if User.objects.filter(username=username):
            continue
        if password is None:
            password = getpass('enter password for user %s: ' % username)
            if password != getpass('reenter password: '):
                raise Exception('password not the same')
        try:
            create_user(username, password, first_name,
                        last_name, email, is_staff=is_staff, is_super=is_super)
        except UserExists:
            pass


def create_owner_base():
    for username in owner_list:
        user = get_user(username=username)
        try:
            create_owner(user)
        except OwnerExists:
            pass


def process_file(device, owner, i):
    name = file_name % {
        'device': device.code_name,
        'num': i
    }
    # yes it hits the database twice, but oh well
    try:
        req = create_request(owner.user, device, name)
    except FileExists:  # raises RequestExists as well, but we won't get that
        return

    t = mkstemp()
    f = open(t[1], 'wb')
    f.write(str.encode(req.reference))
    f.close()
    f = open(t[1], 'rb')
    f = DJFile(f)
    handle_file_upload(f, req)
    f.close()
    os_close(t[0])
    remove(t[1])


def create_file_base():
    print('This will create LOTS of database entries.')
    print('Only do this if you are making a testing server.')
    r = input('Enter "I AM TESTING" to continue: ')
    if r != 'I AM TESTING':
        return
    for device in Device.objects.all():
        for owner in Owner.objects.all():
            for i in range(1, 6):
                process_file(device, owner, i)


if __name__ == '__main__':
    pass