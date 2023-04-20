import unittest

from lazy_copy import copy
from test_state_class import Stateful


class TestLazyCopy(unittest.TestCase):
    def test_literal(self):
        value = 5
        operation = lambda x: x * 3
        state = Stateful(value, operation)
        state_copy = copy(state)
        state_copy.operation()
        self.assertEqual(value, state.value)
        self.assertEqual(operation(value), state_copy.value)