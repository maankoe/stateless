import unittest

from lazy_copy import copy
from test_state_class import Stateful


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
