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
        values = {name: Copied(base, name) for name in ["_value"]}
        properties = {name: getattr(type(base), name) for name in ["value"]}
        functions = {name: Copied(base, name) for name in ["_operation"]}

        child_class = type(
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
                },
                # **{
                #     name: property(
                #         lambda b_self, *args, **kwargs: function.getter()(*args, **kwargs),
                #         lambda b_self, x: function.setter(x)
                #     )
                #     for name, function in functions.items()
                # }
            }
        )
        self.__class__ = child_class

        for name in ["_operation"]:
            setattr(self, name, getattr(base, name))

        for name in ["operation"]:
            setattr(self, name, lambda: getattr(type(base), name)(self))



def copy(base):
    return Copy(base)
