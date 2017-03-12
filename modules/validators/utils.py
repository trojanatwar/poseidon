try: from collections import OrderedDict
except ImportError: from ordereddict import OrderedDict
import inspect, itertools, six
from decorator import decorator

class ValidationFailure(object):
    def __init__(self, func, args):
        self.func = func
        self.__dict__.update(args)

    def __repr__(self):
        return u'ValidationFailure(func={func}, args={args})'.format(
            func=self.func.__name__,
            args=dict(
                [(k, v) for (k, v) in self.__dict__.items() if k != 'func']
            )
        )

    def __str__(self): return repr(self)
    def __unicode__(self): return repr(self)
    def __bool__(self): return False
    def __nonzero__(self): return False

def func_args_as_dict(func, args, kwargs):

    arg_names = list(
        OrderedDict.fromkeys(
            itertools.chain(
                inspect.getargspec(func)[0],
                kwargs.keys()
            )
        )
    )
    return OrderedDict(list(six.moves.zip(arg_names, args)) + list(kwargs.items()))

def validator(func, *args, **kwargs):

    def wrapper(func, *args, **kwargs):
        value = func(*args, **kwargs)
        if not value: return ValidationFailure(func, func_args_as_dict(func, args, kwargs))
        return True
    return decorator(wrapper, func)

