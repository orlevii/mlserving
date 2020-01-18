import json
import unittest

from jarvis.app import Jarvis
from jarvis.app.api import generate_api_v1, generate_models_health_check, InvalidHealthCheck
from tests.common import generate_jarvis_config_with_model, MyTestModel


class JarvisCoreApiV1Test(unittest.TestCase):
    """Test cases for jarvis pre made api/v1"""

    def setUp(self):
        conf = generate_jarvis_config_with_model()

        self.jarvis = Jarvis(conf)

        api_v1 = generate_api_v1()
        self.jarvis.register_router(url='/api/v1',
                                    router=api_v1)

        self.client = self.jarvis.app.test_client()

    def test_pre_made_api_ping(self):
        res = self.client.get('/api/v1/ping')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        expected_text = 'Pong from {}!'.format(self.jarvis.config.service_name)
        self.assertIn(expected_text, result_dict['message'])

    def test_pre_made_api_health(self):
        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        expected_keys = {'health', 'status', 'service_name'}
        self.assertEqual(result_dict.keys(), expected_keys)

    def test_pre_made_api_health_with_error(self):
        expected_results = {
            'status': 'ERROR',
            'message': 'failed'
        }
        self.jarvis.config.health_check_methods = dict(model=self.failing_method)
        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 503)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        method_status = result_dict.get('health', {}).get('model')
        self.assertEqual(method_status, expected_results)

    def test_pre_made_api_health_with_model_check(self):
        expected_results = {
            'status': 'OK'
        }
        my_model = MyTestModel()
        models_instances = [my_model]
        self.jarvis.config.models_instances = models_instances
        self.jarvis.config.health_check_methods = generate_models_health_check(models_instances)
        self.jarvis.load_models()

        res = self.client.get('/api/v1/health')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        method_status = result_dict.get('health', {}).get('MyTestModel')
        self.assertEqual(method_status, expected_results)

    @staticmethod
    def failing_method(**kwargs):
        return InvalidHealthCheck(message='failed')
