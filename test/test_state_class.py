import unittest
from typing import TypeVar, Callable, Generic

from stateless import stateless

T = TypeVar("T")


class Stateful:
    def __init__(self, value: T, operation: Callable[[T], T]):
        self._value = value
        self._operation = operation

    def operation(self):
        self._value = self._operation(self._value)

    @property
    def value(self):
        return self._value


def call_operation(state: Stateful):
    state.operation()


class TestStatefulFunction(unittest.TestCase):
    def test_stateful_class(self):
        value = 3
        operation = lambda x: x * 2
        state = Stateful(value, operation)
        self.assertEqual(3, state.value)
        state.operation()
        self.assertEqual(operation(value), state.value)

    def test_stateful_class_wrapped_stateless(self):
        value = 3
        operation = lambda x: x * 2
        state = Stateful(value, operation)
        stateless(call_operation(state))
        self.assertEqual(operation(value), state.value)