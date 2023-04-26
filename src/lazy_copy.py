import inspect
from typing import Callable


class CopyData:
    def __init__(self, operations):
        for k, v in operations.items():
            setattr(self, k, v)


class Copied:
    def __init__(self, base, name):
        self._base = base
        self._name = name
        self._value = None

    def getter(self):
        if self._value is None:
            return getattr(self._base, self._name)
        else:
            return self._value

    def setter(self, x):
        self._value = x


def is_property(name, member):
    return isinstance(member, property)


def is_function(name, member):
    return inspect.isfunction(member)


def is_method(name, member):
    return inspect.ismethod(member) or inspect.isbuiltin(member) or isinstance(member, Callable) and name != "__class__"


class Copy:
    def __init__(self, base):
        self._base = base
        values = {}
        properties = {}
        functions = {}
        methods = {}
        for name, member in inspect.getmembers(base):
            if is_function(name, member):
                functions[name] = getattr(base, name)
            elif is_method(name, member):
                methods[name] = getattr(type(base), name)
            elif is_property(name, member):
                properties[name] = getattr(type(base), name)
            else:
                values[name] = Copied(base, name)

        self.__class__ = type(
            self.__class__.__name__ + '_COPY',
            (self.__class__,),
            {
                **{
                    name: property(lambda b_self: prop.fget(b_self))
                    for name, prop in properties.items()
                },
                **{
                    name: property(lambda b_self: value.getter(), lambda b_self, x: value.setter(x))
                    for name, value in values.items()
                }
            }
        )

        for name, member in functions.items():
            setattr(self, name, member)

        for name, member in methods.items():
            setattr(self, name, lambda *args, **kwargs: member(self, *args, **kwargs))


def copy(base):
    return Copy(base)
