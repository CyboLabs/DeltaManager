from __future__ import absolute_import

from django.db.models import Field
from django.utils import six
from django.utils.encoding import smart_text

from .validators import Md5Validator


class Md5SumField(Field):
    default_validators = [Md5Validator()]

    def to_python(self, value):
        if isinstance(value, six.string_types) or value is None:
            return value
        return smart_text(value)

    def get_prep_value(self, value):
        value = super(Md5SumField, self).get_prep_value(value)
        return self.to_python(value)

    def get_internal_type(self):
        return 'TextField'

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^api\.v1\.common\.fields\.Md5SumField"])