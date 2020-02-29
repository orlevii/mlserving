import json
import random
import unittest
from unittest.mock import patch

from mest.app import Mest
from mest.app._state import runtime_state
from mest.app.api import Router
from tests.common import generate_mest_config_with_model, MyTestModel


class MestRouterTest(unittest.TestCase):
    """Test cases for mest pre made api/v1"""

    def setUp(self):
        conf = generate_mest_config_with_model()
        self.model_instance = MyTestModel()

        self.mest_app = Mest(conf)

        self.api_v1 = Router('v1')
        self.api_v1.add_ping_route()
        self.api_v1.add_predict_route(self.model_instance,
                                      schema={'user_id': {'type': 'integer', 'required': True}})
        self.mest_app.register_router(url='/api/v1',
                                      router=self.api_v1)

        self.client = self.mest_app.app.test_client()

    def test_pre_made_api_ping(self):
        res = self.client.get('/api/v1/ping')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        expected_text = 'Pong from {}!'.format(self.mest_app.config.service_name)
        self.assertIn(expected_text, result_dict['message'])

    def test_pre_made_api_ping_when_shutting_down(self):
        runtime_state._shutting_down = True
        res = self.client.get('/api/v1/ping')
        self.assertEqual(res.status_code, 503)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        expected_text = 'Pong from {}!'.format(self.mest_app.config.service_name)
        self.assertIn(expected_text, result_dict['message'])
        runtime_state._shutting_down = False

    @patch('tests.common.MyTestModel.predict')
    def test_add_predict(self, mock_predict):
        client = self.mest_app.app.test_client()

        expected_result = 'hello world'
        mock_predict.return_value = expected_result

        random_user_id = random.sample(population=range(10),
                                       k=1)[0]
        res = client.post('/api/v1/predict',
                          data=json.dumps(dict(user_id=random_user_id)),
                          content_type='application/json')

        decoded = res.data.decode('utf-8')
        result_value = json.loads(decoded)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(result_value, expected_result)
        self.assertEqual(mock_predict.call_count, 1)
