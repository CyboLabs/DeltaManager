class BaseExists(Exception):
    msg = "Something exists already"

    def __init__(self, value):
        if not isinstance(value, tuple):
            value = (value,)
        val = "/".join(value)
        message = ": ".join((val, self.msg))
        super(BaseExists, self).__init__(message)
        self.value = val
        self.message = message

    def __str__(self):
        return repr(self.message)


class UserExists(BaseExists):
    msg = "User exists already"


class OwnerExists(BaseExists):
    msg = "Owner exists already"


class ManufacturerExists(BaseExists):
    msg = "Manufacturer exists already"


class DeviceExists(BaseExists):
    msg = "Device exists already"


class FileExists(BaseExists):
    msg = "File exists already"