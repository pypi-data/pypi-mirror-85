from .interception_model import InterceptionVars, Interception
from .exceptions import IllegalStateException, NotFoundException

__all__ = [
    'InterceptionService'
]


class InterceptionService(object):
    def __init__(self, session):
        self.session = session

    def get_vars(self):
        return self.session.query(InterceptionVars).filter_by(id=1).one_or_none()

    def is_active(self):
        v = self.get_vars()
        if v is not None:
            return v.active != 0
        else:
            return True

    def add_interception(self, ps, name, x, trace):
        if self.is_active():
            interception = Interception.of(ps=ps, name=name, x=x, trace=trace)
            self.session.add(interception)
            return interception
        else:
            raise IllegalStateException()

    def set_active(self, value):
        v = self.get_vars()
        if v is not None:
            v.active = 1 if value else 0
            self.session.add(v)
        else:
            raise NotFoundException
