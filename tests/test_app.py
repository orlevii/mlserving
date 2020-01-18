import json
import random
import unittest

from jarvis.app import Jarvis
from jarvis.app.api import Router, validate_params
from tests.common import generate_jarvis_config_with_model, MyTestModel
from unittest.mock import patch


class JarvisCoreAppTest(unittest.TestCase):
    """Test cases for jarvis application setup"""

    def setUp(self):
        conf = generate_jarvis_config_with_model()

        self.jarvis = Jarvis(conf)

    def test_load_models(self):
        test_model = MyTestModel()
        test_model.model = None

        self.jarvis.config.models_instances = [test_model]
        self.jarvis.load_models()

        expected_result = '42'

        self.assertEqual(test_model.model, expected_result)

    def test_add_api(self):
        router = Router('v1')
        expected_result = 'Hello World'

        @router.route(url='ping', method='GET')
        def ping_method():
            return expected_result

        self.jarvis.register_router(url='/api/v1',
                                    router=router)

        client = self.jarvis.app.test_client()

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

        self.jarvis.register_router(url='/api/v1',
                                    router=router)

        client = self.jarvis.app.test_client()

        expected_value = random.sample(population=range(10),
                                       k=1)[0]
        res = client.post('/api/v1/predict',
                          data=json.dumps(dict(value=expected_value)),
                          content_type='application/json')
        self.assertEqual(res.status_code, 200)

        decoded = res.data.decode('utf-8')
        result_dict = json.loads(decoded)
        self.assertEqual(result_dict['prediction'], expected_value)

    @patch('tests.common.MyTestModel.predict')
    def test_add_predict(self, mock_predict):
        test_model = MyTestModel()
        test_model.model = None

        self.jarvis.config.models_instances = [test_model]
        self.jarvis.load_models()

        router = Router('v1')

        router.simple_predict(model_instance=test_model,
                              schema={'user_id': {'type': 'integer', 'required': True}})

        self.jarvis.register_router(url='/api/v1',
                                    router=router)

        client = self.jarvis.app.test_client()

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
