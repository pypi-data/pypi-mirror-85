import abc
import datetime
import time

from .types import Undefined

_DEFAULT_SLEEP_TIME = 0.2


class DriverBase(object, metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    def run_test(self, name, args):
        test_method = getattr(self, name)
        if callable(test_method):
            return test_method(**args)
        else:
            raise ValueError(f'test_method {name} is not callable')


class StateBase(object, metaclass=abc.ABCMeta):
    def __init__(self):
        self.ignore_undefined = True

    @property
    @abc.abstractmethod
    def state_props(self):
        pass

    def compare(self, **kwargs):
        for arg_name, arg_value in kwargs.items():
            if arg_name in self.state_props:
                value = self.__dict__[arg_name]
                if not Undefined.is_undefined(arg_value) and not Undefined.is_undefined(value):
                    if value != arg_value:
                        return False
            else:
                raise ValueError(f'prop {arg_name} is not in state_props')
        return True

    @property
    def values_dict(self):
        r = {}
        for state_prop in self.state_props:
            r[state_prop] = self.__dict__[state_prop]
        return r

    def compare_with(self, other):
        kwargs = other.values_dict
        return self.compare(**kwargs)


class WaitState(object):
    def __init__(self):
        pass

    @staticmethod
    def wait_while(condition, supplier, timeout, sleep_time=_DEFAULT_SLEEP_TIME):
        start_time = datetime.datetime.now()
        elapsed_time = datetime.datetime.now() - start_time
        result = False
        while elapsed_time.seconds < timeout:
            state_entities = supplier()
            if not isinstance(state_entities, list) and not isinstance(state_entities, tuple):
                state_entities = [state_entities]
            result = condition(*state_entities)
            if result:
                break
            time.sleep(sleep_time)
            elapsed_time = datetime.datetime.now() - start_time
        return result


class ObserverBase(object, metaclass=abc.ABCMeta):
    def __init__(self):
        pass
