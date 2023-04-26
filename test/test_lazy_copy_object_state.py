import unittest
from typing import Callable

from lazy_copy import copy


class State:
    def __init__(self, value: int):
        self.value = value


class Stateful:
    def __init__(self, state: State, operation: Callable[[int], int]):
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


value = 5
operation = lambda x: x * 3
identity = lambda x: x


class TestObjectState(unittest.TestCase):
    def test_object_stateless(self):
        stateful = Stateful(State(value), operation)
        stateful_copy = copy(stateful)
        stateful_copy.operation()
        self.assertEqual(value, stateful.state.value, "Underlying changed")
        self.assertEqual(operation(value), stateful_copy.state.value, "Copy didn't change")
        # is_property(stateful.state) == false, so it gets handled as a value.
        # isinstance(type(base).state, property) == true though!
