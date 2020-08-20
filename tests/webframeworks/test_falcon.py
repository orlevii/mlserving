import unittest

from .framework_tester import BaseFrameworkTester


class FalconFrameworkTest(BaseFrameworkTester, unittest.TestCase):
    """Test cases for falcon web-framework"""
    FRAMEWORK = 'falcon'
