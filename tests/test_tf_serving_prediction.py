import unittest
from random import random
from unittest.mock import patch

from mlserving.predictors.tensorflow import TFServingPrediction, TFServingRequestError


class ResponseMock:
    def __init__(self, status_code=200):
        self.status_code = status_code
        self.content = b'some content'

    def json(self):
        return {}


class TFServingPredictionTest(unittest.TestCase):

    def setUp(self):
        self.payload = {
            'instances': [
                [random(), random(), random()]
            ]
        }

    @patch('requests.post', return_value=ResponseMock())
    def test_url_builder(self, post_mock):
        expected_result = 'http://localhost:1234/v1/models/test_model:predict'
        p = TFServingPrediction(host='localhost', port=1234, model_name='test_model')
        p.predict(self.payload, None)

        self.assertEqual(expected_result, p.predict_api_url)
        post_mock.assert_called_with(expected_result, json=self.payload)

    @patch('requests.post', return_value=ResponseMock())
    def test_url(self, post_mock):
        expected_result = 'http://10.10.10.10:4321/v1/models/my_test_model:predict'
        p = TFServingPrediction(predict_api_url=expected_result)
        p.predict(self.payload, None)

        self.assertEqual(expected_result, p.predict_api_url)
        post_mock.assert_called_with(expected_result, json=self.payload)

    @patch('requests.post', return_value=ResponseMock(400))
    def test_tf_serving_error(self, post_mock):
        p = TFServingPrediction()
        with self.assertRaises(TFServingRequestError) as e:
            p.predict(self.payload, None)
