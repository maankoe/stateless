# Need a better name for this, it's kind of "seemingly/apparently frozen/static/stateful"
# Would nice to have 'normal' operations applied to a duplicate/copy object, but be able to access the
#  original when wanted by the 'user'
from stateless import stateless

class Wrap:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __mul__(self, other):
        return self._value * other


class Copy:
    def __init__(self, base):
        self._base = base
        self._value = self._base.value
        self._operation = base._operation
        self.copy_operation = type(base).operation
        self.operation = lambda: self.copy_operation(self)
        # type(self).value = property(lambda self: self._value)

        class_name = self.__class__.__name__ + 'Child'
        child_class = type(class_name, (self.__class__,), {"value": property(lambda self: self._value)})
        self.__class__ = child_class

def copy(base):
    return Copy(base)
