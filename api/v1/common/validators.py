from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class Md5Validator(object):
    message = _('Enter a valid md5sum.')
    code = 'invalid'

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = None
        if code is not None:
            self.code = code

    def __call__(self, value):
        """call function

        first check the length.

        the next stage checks that `value` is hexadecimal.
        normally, you compare each character in a for loop, which
        takes time (2s for 500,000 loops).
        the next option is using `int(value, 16)`, however on a
        failure, this takes time (1.3s for 500,000 loops).
        float.fromhex gives the best performance
        (0.3s for 500,000 loops) for both success and failure.
        """
        # more efficient to check the length first
        if not len(value) == 32:
            raise ValidationError(self.message, self.code)

        try:
            float.fromhex(value)
        except ValueError:
            raise ValidationError(self.message, self.code)

    def __eq__(self, other):
        return (
            isinstance(other, Md5Validator) and
            self.message == other.message and
            self.code == other.code
        )

    def __ne__(self, other):
        return not self.__eq__(other)