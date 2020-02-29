import json
import random
import unittest

from mest.app import Mest
from mest.app.api import Router, validate_params
from tests.common import generate_mest_config_with_model, MyTestModel
from unittest.mock import patch


class MestCoreAppTest(unittest.TestCase):
    """Test cases for mest application setup"""

    def setUp(self):
        conf = generate_mest_config_with_model()

        self.mest = Mest(conf)

    def test_load_models(self):
        test_model = MyTestModel()
        test_model.model = None

        self.mest.config.models_instances = [test_model]
        self.mest.load_models()

        expected_result = '42'

        self.assertEqual(test_model.model, expected_result)

    def test_add_api(self):
        router = Router('v1')
        expected_result = 'Hello World'

        @router.route(url='ping', method='GET')
        def ping_method():
            return expected_result

        self.mest.register_router(url='/api/v1',
                                  router=router)

        client = self.mest.app.test_client()

        res = client.get('/api/v1/ping')
        self.assertEqual(res.status_code, 200)

        response = res.data.decode('utf-8')
        self.assertEqual(response, expected_result)

    def test_add_api_with_schema(self):
        router = Router('v1')

        @router.route(url='predict')
        @validate_params({'value': {'type': 'integer', 'required': False, 'default': 5}})
        def predict(value, **params):
            return json.dumps({
                'prediction': value
            })

        self.mest.register_router(url='/api/v1',
                                  router=router)

        client = self.mest.app.test_client()

        expected_value = random.sample(population=range(10),
                                       k=1)[0]
        res = client.post('/api/v1/predict',
                          data=json.dumps(dict(value=expected_value)),
                          content_type='application/json')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        self.assertEqual(result_dict['prediction'], expected_value)
