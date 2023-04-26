import unittest
from typing import Callable

from lazy_copy import copy


class Stateful:
    def __init__(self, value: int, operation: Callable[[int, int], int]):
        self._value = value
        self._operation = operation

    def operation(self, arg: int):
        new_value = self._operation(self._value, arg)
        if new_value == self._value:
            raise ValueError("The operation did not change the state.")
        self._value = new_value

    @property
    def value(self):
        return self._value


value = 3
arg = 11
operation = lambda x, y: x * y
identity = lambda x, y: x


class TestLazyCopyArgs(unittest.TestCase):
    def test_arg(self):
        state = Stateful(value, operation)
        state_copy = copy(state)
        state_copy.operation(arg)
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value, arg), state_copy.value, "Copy didn't change")

    def test_kwarg(self):
        state = Stateful(value, operation)
        state_copy = copy(state)
        state_copy.operation(arg=arg)
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value, arg), state_copy.value, "Copy didn't change")

    def test_stateful_class(self):
        state = Stateful(value, operation)
        self.assertEqual(value, state.value)
        state.operation(arg)
        self.assertEqual(operation(value, arg), state.value)

    def test_throws_when_no_change(self):
        state = Stateful(value, identity)
        self.assertRaises(ValueError, lambda: state.operation(arg))
