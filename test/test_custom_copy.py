import unittest
from unittest.mock import Mock

from stateless import stateless
from test_general import stateful_function


class TestCustomCopy(unittest.TestCase):
    def test_uniform_copy(self):
        arg = [1, 2, 3]
        arg_copy = [x for x in arg]
        mock_copy = Mock()
        stateless(stateful_function, copy_func=mock_copy)(arg)
        mock_copy.assert_called_with(arg)
        self.assertEqual(arg_copy, arg)

    def test_arg_specific_copy(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_a_copy = [x for x in arg_a]
        arg_b_copy = [x for x in arg_b]
        mock_copy_a = Mock()
        mock_copy_b = Mock()
        stateless(stateful_function, arg_copy_funcs=[mock_copy_a, mock_copy_b])(arg_a, arg_b)
        mock_copy_a.assert_called_with(arg_a)
        mock_copy_b.assert_called_with(arg_b)
        self.assertEqual(arg_a_copy, arg_a)
        self.assertEqual(arg_b_copy, arg_b)

    def test_kwarg_specific_copy(self):
        arg_a = [1, 2, 3]
        arg_b = ["a", "b", "c"]
        arg_a_copy = [x for x in arg_a]
        arg_b_copy = [x for x in arg_b]
        mock_copy_a = Mock()
        mock_copy_b = Mock()
        stateless(stateful_function, arg_copy_funcs={"x": mock_copy_a, "y": mock_copy_b})(x=arg_a, y=arg_b)
        mock_copy_a.assert_called_with(arg_a)
        mock_copy_b.assert_called_with(arg_b)
        self.assertEqual(arg_a_copy, arg_a)
        self.assertEqual(arg_b_copy, arg_b)
