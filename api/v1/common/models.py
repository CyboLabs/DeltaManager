from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models

from .fields import Md5SumField
from eos.settings import DOWNLOAD_URL

from os.path import join


class Owner(models.Model):
    user = models.OneToOneField(User, unique=True, related_name='user')

    def can_edit(self, user):
        return self.user == user or user.is_admin

    def total_uploads(self):
        return len(File.objects.filter(owner=self))

    def worked_on_devices(self):
        file_list = File.objects.filter(owner=self)
        return file_list.values_list('device')

    def __str__(self):
        return self.user.username


class Manufacturer(models.Model):
    code_name = models.CharField(max_length=25)
    full_name = models.CharField(max_length=25)

    def can_edit(self, user):
        return user.is_admin

    def devices(self):
        return Device.objects.filter(manufacturer=self)

    def __str__(self):
        return self.full_name


class Device(models.Model):
    code_name = models.CharField(max_length=10)
    full_name = models.CharField(max_length=25)
    manufacturer = models.ForeignKey('Manufacturer', related_name='manufacturer')

    def can_edit(self, user):
        return user.is_admin

    def total_uploads(self):
        return len(File.objects.filter(device=self))

    def __str__(self):
        return self.full_name


class File(models.Model):
    owner = models.ForeignKey('Owner', related_name='owner')
    device = models.ForeignKey('Device', related_name='device')
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True, null=True)
    size = models.PositiveIntegerField()
    download_count = models.PositiveIntegerField(default=0)
    md5sum = Md5SumField()
    # for Deltas
    old_version = models.CharField(max_length=20, blank=True, null=True)

    def can_edit(self, user):
        return user == self.owner.user or user.is_admin

    def get_public_url(self):
        # adding the name does nothing for the logic
        # it's a quick hack to make wget work properly
        url = join('/api/v1/files/download/', str(self.id), self.name)
        return url

    def get_direct_url(self):
        url = DOWNLOAD_URL % {
            'name': self.name,
            'owner': self.owner.user.username,
            'device': self.device.code_name
        }
        return url

    def __str__(self):
        return self.name


class RequestUpload(models.Model):
    owner = models.ForeignKey('Owner')
    device = models.ForeignKey('Device')
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20, blank=True, null=True)
    old_version = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=32)