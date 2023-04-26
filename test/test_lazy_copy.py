import unittest

from lazy_copy import copy
from test_state_class import Stateful, ParamStateful


class TestLazyCopy(unittest.TestCase):
    def test_literal_stateless(self):
        value = 5
        operation = lambda x: x * 3
        state = Stateful(value, operation)
        state_copy = copy(state)
        state_copy.operation()
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value), state_copy.value, "Copy didn't change")

    def test_copy_has_values(self):
        value = 5
        operation = lambda x: x * 3
        state = Stateful(value, operation)
        state_copy = copy(state)
        self.assertEqual(value, state_copy._value)
        self.assertEqual(operation, state_copy._operation)

    def test_copy_has_properties(self):
        value = 5
        state = Stateful(value, lambda x: x * 3)
        state_copy = copy(state)
        self.assertEqual(value, state_copy.value)

    def test_object_stateless(self):
        class Box:
            def __init__(self, _value):
                self._value = _value

            def mul(self, x):
                return Box(self._value * x)

        box_value = Box(4)
        operation = lambda box: box.mul(10)
        state = Stateful(box_value, operation)
        state_copy = copy(state)
        state_copy.operation()
        self.assertEqual(box_value, state.value, "Underlying changed")
        self.assertEqual(operation(box_value)._value, state_copy.value._value, "Copy didn't change")


    def test_literal_param_stateless_arg(self):
        value = 5
        arg = 3
        operation = lambda x, y: x * y
        state = ParamStateful(value, operation)
        state_copy = copy(state)
        state_copy.operation(arg)
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value, arg), state_copy.value, "Copy didn't change")

    def test_literal_param_stateless_kwarg(self):
        value = 5
        arg = 3
        operation = lambda x, y: x * y
        state = ParamStateful(value, operation)
        state_copy = copy(state)
        state_copy.operation(arg=arg)
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value, arg), state_copy.value, "Copy didn't change")
