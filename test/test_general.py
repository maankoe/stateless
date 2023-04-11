import unittest
from typing import Any


def stateful_function(*args: list[Any], **kwargs: list[Any]) -> None:
    for arg in args:
        arg.clear()
    for arg in kwargs.values():
        arg.clear()


class TestGeneral(unittest.TestCase):
    def test_stateful_function(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_c = [5, 6, 7]
        arg_d = ["d", "e", "f"]
        stateful_function(arg_a, arg_b, x=arg_c, y=arg_d)
        self.assertEqual([], arg_a)
        self.assertEqual([], arg_b)
        self.assertEqual([], arg_c)
        self.assertEqual([], arg_d)
