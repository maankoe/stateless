import unittest
from typing import Callable, Generic, TypeVar

from lazy_copy import copy


T = TypeVar("T")


class State(Generic[T]):
    def __init__(self, value: T):
        self.value = value


class Stateful(Generic[T]):
    def __init__(self, state: State, operation: Callable[[T], T]):
        self._state = state
        self._operation = operation

    def operation(self):
        new_value = self._operation(self._state.value)
        if new_value == self._state.value:
            raise ValueError("The operation did not change the state.")
        self._state.value = new_value

    @property
    def state(self):
        return self._state


operation = lambda x: x * 3


class TestObjectState(unittest.TestCase):
    def test_object_stateless_int(self):
        value = int(11)
        stateful = Stateful(State(value), operation)
        stateful_copy = copy(stateful)
        stateful_copy.operation()
        self.assertEqual(value, stateful.state.value, "Underlying changed")
        self.assertEqual(operation(value), stateful_copy.state.value, "Copy didn't change")

    def test_object_stateless_float(self):
        value = float(12.4)
        stateful = Stateful(State(value), operation)
        stateful_copy = copy(stateful)
        stateful_copy.operation()
        self.assertEqual(value, stateful.state.value, "Underlying changed")
        self.assertEqual(operation(value), stateful_copy.state.value, "Copy didn't change")

    def test_object_stateless_str(self):
        value = str("HELLO WORLD")
        stateful = Stateful(State(value), operation)
        stateful_copy = copy(stateful)
        stateful_copy.operation()
        self.assertEqual(value, stateful.state.value, "Underlying changed")
        self.assertEqual(operation(value), stateful_copy.state.value, "Copy didn't change")
