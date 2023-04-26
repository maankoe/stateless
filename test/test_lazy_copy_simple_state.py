import unittest
from typing import Callable
from lazy_copy import copy


class Stateful:
    def __init__(self, value: int, operation: Callable[[int], int]):
        self._value = value
        self._operation = operation

    def operation(self):
        new_value = self._operation(self._value)
        if new_value == self._value:
            raise ValueError("The operation did not change the state.")
        self._value = new_value

    @property
    def value(self):
        return self._value


value = 5
operation = lambda x: x * 3
identity = lambda x: x


class TestLazyCopySimpleState(unittest.TestCase):
    def test_literal_stateless(self):
        state = Stateful(value, operation)
        state_copy = copy(state)
        state_copy.operation()
        self.assertEqual(value, state.value, "Underlying changed")
        self.assertEqual(operation(value), state_copy.value, "Copy didn't change")

    def test_copy_has_values(self):
        state = Stateful(value, operation)
        state_copy = copy(state)
        self.assertEqual(value, state_copy._value)
        self.assertEqual(operation, state_copy._operation)

    def test_copy_has_properties(self):
        state = Stateful(value, operation)
        state_copy = copy(state)
        self.assertEqual(value, state_copy.value)

    def test_stateful_class(self):
        state = Stateful(value, operation)
        self.assertEqual(value, state.value)
        state.operation()
        self.assertEqual(operation(value), state.value)

    def test_stateful_throws_when_no_change(self):
        state = Stateful(value, identity)
        self.assertRaises(ValueError, lambda: state.operation())
