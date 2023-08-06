import unittest

from .base import DriverBase


class CustomDriver(DriverBase):
    def __init__(self):
        DriverBase.__init__(self)
        self.arg0 = None
        self.arg1 = None

    def test_any(self, arg0, arg1):
        self.arg0 = arg0
        self.arg1 = arg1


class BaseDriverTests(unittest.TestCase):
    def setUp(self):
        self.custom_driver = CustomDriver()

    def test_run_test(self):
        self.custom_driver.run_test('test_any', args={'arg0': 'test0', 'arg1': 'test1'})
        self.assertEqual('test0', self.custom_driver.arg0)
        self.assertEqual('test1', self.custom_driver.arg1)
