import unittest

from .types import Undefined


class UndefinedTests(unittest.TestCase):
    def test_is_undefined(self):
        value = Undefined()
        result = Undefined.is_undefined(value)
        self.assertTrue(result)
