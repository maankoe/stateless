import unittest
from typing import TypeVar, Callable, Generic, Any

from stateless import stateless

T = TypeVar("T")


class Stateful:
    def __init__(self, value: T, operation: Callable[[T], T]):
        self._value = value
        self._operation = operation

    def operation(self):
        new_value = self._operation(self._value)
        if new_value == self._value:
            raise ValueError("The operation did not change the state.")
        self._value = self._operation(self._value)

    @property
    def value(self):
        return self._value


class ParamStateful:
    def __init__(self, value: T, operation: Callable[[T, Any], T]):
        self._value = value
        self._operation = operation

    def operation(self, arg: Any):
        new_value = self._operation(self._value, arg)
        if new_value == self._value:
            raise ValueError("The operation did not change the state.")
        self._value = self._operation(self._value, arg)

    @property
    def value(self):
        return self._value


class TestStatefulClass(unittest.TestCase):
    def test_stateful_class(self):
        value = 3
        operation = lambda x: x * 2
        state = Stateful(value, operation)
        self.assertEqual(3, state.value)
        state.operation()
        self.assertEqual(operation(value), state.value)

    def test_stateful_class_wrapped_stateless(self):
        def call_operation(state: Stateful):
            state.operation()

        value = 3
        operation = lambda x: x * 2
        state = Stateful(value, operation)
        stateless(call_operation(state))
        self.assertEqual(operation(value), state.value)

    def test_stateful_throws_when_no_change(self):
        state = Stateful(2, lambda x: x)
        self.assertRaises(ValueError, lambda: state.operation())

    def test_param_stateful_class(self):
        value = 3
        arg = 6
        operation = lambda x, arg: x * arg
        state = ParamStateful(value, operation)
        self.assertEqual(3, state.value)
        state.operation(arg)
        self.assertEqual(operation(value, arg), state.value)

    def test_param_stateful_class_wrapped_stateless(self):
        def call_operation(state: ParamStateful, arg: int):
            state.operation(arg)

        value = 3
        arg = 2
        operation = lambda x, arg: x * arg
        state = ParamStateful(value, operation)
        stateless(call_operation(state, arg))
        self.assertEqual(operation(value, arg), state.value)

    def test_param_stateful_throws_when_no_change(self):
        state = ParamStateful(2, lambda x, arg: x)
        self.assertRaises(ValueError, lambda: state.operation(3))
