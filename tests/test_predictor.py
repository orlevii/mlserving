import unittest

from tests.common import MyTestModel


class MestPredictorTest(unittest.TestCase):
    """Test cases for mest "predictors" & "models" setup"""

    def setUp(self):
        pass

    def test_simple_predict(self):
        expected_result = '42'
        test_model = MyTestModel()
        result = test_model.create_predictor().predict(None)

        self.assertEqual(result.data, expected_result)
