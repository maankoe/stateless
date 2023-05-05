import logging
import inspect
from typing import Callable

__all__ = ["copy"]

logger = logging.getLogger(__file__)


class DeferredCopy:
    def __init__(self, base, name):
        self._base = base
        self._name = name
        self._value = None

    def getter(self):
        logger.debug(f"Deferred: GETTER {self._name}")
        if self._value is None:
            value = getattr(self._base, self._name)
            if _is_primitive(value):
                self._value = value
            else:
                self._value = copy(value)
        return self._value

    def setter(self, x):
        logger.debug(f"Deferred: SETTER {self._name}")
        self._value = x


_primitive_types = {int, float, str}


def _is_primitive(instance):
    return type(instance) in _primitive_types


def _is_property(name, member):
    return isinstance(member, property)


def _is_function(name, member):
    return inspect.isfunction(member)


def _is_method(name, member):
    return inspect.ismethod(member) or inspect.isbuiltin(member) or isinstance(member, Callable) and name != "__class__"


def _gather_class_members(base, captured):
    methods, properties = {}, {}
    for name, member in inspect.getmembers(type(base)):
        logger.debug(f"classmember: {name}, {member}")
        if _is_method(name, member):
            methods[name] = getattr(type(base), name)
        elif _is_property(name, member):
            properties[name] = getattr(type(base), name)
        captured.add(name)
    return methods, properties


def _gather_instance_members(base, captured):
    functions, values = {}, {}
    for name, member in inspect.getmembers(base):
        if name in captured:
            continue
        logger.debug(f"instanncemember: {name}, {member}")
        if _is_function(name, member):
            functions[name] = getattr(base, name)
        else:
            values[name] = DeferredCopy(base, name)
        captured.add(name)
    return functions, values


def _make_values(values):
    return {
        name: property(lambda b_self: value.getter(), lambda b_self, x: value.setter(x))
        for name, value in values.items()
    }


def _make_properties(properties):
    return {
        name: property(lambda b_self: prop.fget(b_self))
        for name, prop in properties.items()
    }


class Copy:
    def __init__(self, base):
        logger.debug(f"---COPY--- {type(base)}")
        self._base = base
        captured = set()
        methods, properties = _gather_class_members(base, captured)
        functions, values = _gather_instance_members(base, captured)

        self._setup_class(methods, properties, functions, values)

    def _setup_class(self, methods, properties, functions, values):
        self.__class__ = type(
            self.__class__.__name__ + '_COPY',
            (self.__class__,),
            {**_make_properties(properties), **_make_values(values)}
        )
        self._setup_methods(methods)
        self._setup_functions(functions)

    def _setup_methods(self, methods):
        for name, member in methods.items():
            setattr(self, name, lambda *args, **kwargs: member(self, *args, **kwargs))

    def _setup_functions(self, functions):
        for name, member in functions.items():
            setattr(self, name, member)


def copy(base):
    return Copy(base)
