import unittest

from mest.api import Request
from mest.predictors import RESTPredictor
from mest.predictors.runner import PredictorRunner


class TestPredictor(RESTPredictor):

    def predict(self, processed_data, req: Request):
        return '42'


class MestPredictorTest(unittest.TestCase):
    """Test cases for mest "predictors" & "models" setup"""

    def setUp(self):
        pass

    def test_simple_predict(self):
        expected_result = '42'
        result = PredictorRunner.run_inference(TestPredictor(), Request(payload={}))

        self.assertEqual(result.data, expected_result)
