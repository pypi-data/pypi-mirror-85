import os

from .exceptions import ArgumentException

__all__ = [
    'get_or_env',
    'first_existent_path',
    'get_or_else'
]


def get_or_env(value, name):
    if value is not None:
        return value
    return os.environ.get(name)


def first_existent_path(sources):
    if not sources:
        raise ArgumentException()
    for source in sources:
        if os.path.exists(source):
            return source
    return None


def get_or_else(value, other=None):
    if value is not None:
        return value
    return other

