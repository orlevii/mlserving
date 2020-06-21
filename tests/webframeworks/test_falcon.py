import unittest

from .framework_tester import BaseFrameworkTester


class MestFalconTest(BaseFrameworkTester, unittest.TestCase):
    """Test cases for falcon web-framework"""
    FRAMEWORK = 'falcon'
