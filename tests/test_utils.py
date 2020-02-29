import unittest

from mest.utils import singleton

PROP_VALUE = 10


class MestCoreUtilsTest(unittest.TestCase):
    """Test cases for mest utils"""

    def setUp(self):
        pass

    def test_singleton(self):
        obj1 = MyClass()
        new_value = PROP_VALUE * 2
        obj1.prop = new_value

        obj2 = MyClass()

        self.assertEqual(obj1, obj2)
        self.assertEqual(obj2.prop, new_value)

    def test_2_singletons(self):
        a = MyClass()
        b = MyOtherClass()

        self.assertNotEqual(a, b)
        self.assertNotEqual(type(a), type(b))


@singleton()
class MyClass(object):
    def __init__(self):
        self.prop = 0


@singleton()
class MyOtherClass(object):
    def __init__(self):
        self.x = 0
        self.y = 0
