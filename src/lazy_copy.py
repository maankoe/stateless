# Need a better name for this, it's kind of "seemingly/apparently frozen/static/stateful"
# Would nice to have 'normal' operations applied to a duplicate/copy object, but be able to access the
#  original when wanted by the 'user'
from inspect import getmembers
from stateless import stateless


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


class Copy:
    def __init__(self, base):
        self._base = base

        self._operation = base._operation

        # methods = {name: getattr(type(base), name) for name in ["operation"]}
        # values = {name: Copied(base, name) for name in ["_value", "_operation"]}

        for name in ["operation"]:
            setattr(self, name, lambda: getattr(type(base), name)(self))

        self._value_copy = Copied(base, "_value")

        child_class = type(
            self.__class__.__name__ + '_COPY',
            (self.__class__,),
            {
                "value": property(lambda b_self: getattr(type(base), "value").fget(b_self)),
                "_value": property(
                    lambda b_self: b_self._value_copy.getter(),
                    lambda b_self, x: b_self._value_copy.setter(x),
                )
            }
        )
        self.__class__ = child_class


def copy(base):
    return Copy(base)
