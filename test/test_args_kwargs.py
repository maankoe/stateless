import unittest
from typing import Any

from stateless import stateless


def stateful_function(*args: list[Any], **kwargs: list[Any]) -> None:
    for arg in args:
        arg.clear()
    for arg in kwargs.values():
        arg.clear()


class TestArgsKwargs(unittest.TestCase):
    def test_stateful_function(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_c = [5, 6, 7]
        arg_d = ["d", "e", "f"]
        stateful_function(arg_a, arg_b, x=arg_c, y=arg_d)
        self.assertEqual(arg_a, [])
        self.assertEqual(arg_b, [])
        self.assertEqual(arg_c, [])
        self.assertEqual(arg_d, [])

    def test_single_arg(self):
        arg = [1, 2, 3]
        arg_copy = [x for x in arg]
        stateless(stateful_function)(arg)
        self.assertEqual(arg, arg_copy)

    def test_multi_arg(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_a_copy = [x for x in arg_a]
        arg_b_copy = [x for x in arg_b]
        stateless(stateful_function)(arg_a, arg_b)
        self.assertEqual(arg_a, arg_a_copy)
        self.assertEqual(arg_b, arg_b_copy)

    def test_kwarg(self):
        arg = [1, 2, 3]
        arg_copy = [x for x in arg]
        stateless(stateful_function)(x=arg)
        self.assertEqual(arg, arg_copy)

    def test_multi_kwarg(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_a_copy = [x for x in arg_a]
        arg_b_copy = [x for x in arg_b]
        stateless(stateful_function)(x=arg_a, y=arg_b)
        self.assertEqual(arg_a, arg_a_copy)
        self.assertEqual(arg_b, arg_b_copy)

    def test_arg_kwarg(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_c = [5, 6, 7]
        arg_d = ["d", "e", "f"]
        arg_a_copy = [x for x in arg_a]
        arg_b_copy = [x for x in arg_b]
        arg_c_copy = [x for x in arg_c]
        arg_d_copy = [x for x in arg_d]
        stateless(stateful_function)(arg_a, arg_b, x=arg_c, y=arg_d)
        self.assertEqual(arg_a, arg_a_copy)
        self.assertEqual(arg_b, arg_b_copy)
        self.assertEqual(arg_c, arg_c_copy)
        self.assertEqual(arg_d, arg_d_copy)
