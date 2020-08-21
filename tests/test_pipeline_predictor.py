import unittest
from random import random

from mlserving.api import Request, request_schema
from mlserving.predictors import PipelinePredictor, RESTPredictor
from mlserving.predictors.runner import PredictorRunner

A_SCHEMA = {
    'age': 'float'
}
B_SCHEMA = {
    'score': 'float'
}


@request_schema(A_SCHEMA)
class PredictorA(RESTPredictor):
    ERROR_MSG = 'invalid age'

    def predict(self, processed_data, req: Request):
        if processed_data['age'] <= 0:
            raise RuntimeError(self.ERROR_MSG)
        return {'score': processed_data['age'] / 2}


@request_schema(B_SCHEMA)
class PredictorB(RESTPredictor):

    def predict(self, processed_data, req: Request):
        return {'result': processed_data['score'] ** 2}


class PipelinePredictorTest(unittest.TestCase):
    """Test cases for mlserving "predictors" & "models" setup"""

    def setUp(self):
        self.predictor = PipelinePredictor([PredictorA(), PredictorB()])

    def test_successful_predict(self):
        input_age = random() * 100
        expected_result = dict(result=(input_age / 2) ** 2)
        result = PredictorRunner.run_inference(self.predictor,
                                               Request(payload={'age': input_age}))

        self.assertEqual(result.data, expected_result)

    def test_failed_predict(self):
        result = PredictorRunner.run_inference(self.predictor,
                                               Request(payload={'age': 0}))

        self.assertEqual(result.get_status_code(), 500)
        self.assertEqual(result.data, {'error': PredictorA.ERROR_MSG})
