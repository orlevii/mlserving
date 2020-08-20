import unittest

from mlserving.api import Request
from mlserving.predictors import RESTPredictor
from mlserving.predictors.runner import PredictorRunner


class TestPredictor(RESTPredictor):

    def predict(self, processed_data, req: Request):
        return '42'


class RESTPredictorTest(unittest.TestCase):
    """Test cases for mlserving "predictors" & "models" setup"""

    def setUp(self):
        pass

    def test_simple_predict(self):
        expected_result = '42'
        result = PredictorRunner.run_inference(TestPredictor(), Request(payload={}))

        self.assertEqual(result.data, expected_result)
