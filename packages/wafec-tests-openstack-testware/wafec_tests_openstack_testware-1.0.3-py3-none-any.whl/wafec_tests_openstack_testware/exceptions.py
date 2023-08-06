import abc

__all__ = [
    'NotFoundException',
    'StateMismatchException',
    'ArgumentException',
    'IllegalStateException',
    'ExceptionBase'
]


class ExceptionBase(Exception, metaclass=abc.ABCMeta):
    pass


class NotFoundException(ExceptionBase):
    pass


class StateMismatchException(ExceptionBase):
    pass


class ArgumentException(ExceptionBase):
    pass


class IllegalStateException(ExceptionBase):
    pass
