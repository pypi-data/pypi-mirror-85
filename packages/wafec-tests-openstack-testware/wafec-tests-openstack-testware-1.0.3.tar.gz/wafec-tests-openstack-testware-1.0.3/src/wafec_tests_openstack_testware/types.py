

class Undefined(object):
    @staticmethod
    def is_undefined(value):
        return value is not None and issubclass(type(value), Undefined)
