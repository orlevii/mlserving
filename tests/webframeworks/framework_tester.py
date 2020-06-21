import threading
from random import random

import requests

from mest import Mest
from tests.common import create_test_server
from tests.complex_model import MyModel
from tests.error_model import FailModel


class BaseFrameworkTester:
    """Test cases for mest web-frameworks"""
    FRAMEWORK = None

    mest = None
    port = None
    test_server = None

    @classmethod
    def setUpClass(cls):
        cls.mest = Mest(framework=cls.FRAMEWORK)
        cls.mest.add_health_handler(MyModel(), '/api/v1/health')
        cls.mest.add_inference_handler(MyModel(), '/api/v1/predict')
        cls.mest.add_health_handler(FailModel(), '/api/v1/health_error')
        cls.mest.add_inference_handler(FailModel(), '/api/v1/predict_error')
        cls.test_server = create_test_server(cls.mest.app)
        cls.port = cls.test_server.server_port
        t = threading.Thread(target=cls.test_server.serve_forever)
        t.start()

    def setUp(self):
        self.health_url = f'http://localhost:{self.port}/api/v1/health'
        self.fail_health_url = f'http://localhost:{self.port}/api/v1/health_error'
        self.inference_route = f'http://localhost:{self.port}/api/v1/predict'
        self.fail_inference_route = f'http://localhost:{self.port}/api/v1/predict_error'

    def test_health_route(self):
        response = requests.get(self.health_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'ok'})

    def test_inference_route(self):
        req_data = dict(
            feature1=random(),
            feature2=random(),
            feature3=random()
        )
        expected_result = {'score': sum(req_data.values())}

        response = requests.post(self.inference_route, json=req_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_health_route_with_error(self):
        response = requests.get(self.fail_health_url)
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'message': FailModel.HEALTH_ERROR})

    def test_inference_route_with_error(self):
        req_data = {}

        response = requests.post(self.fail_inference_route, json=req_data)
        self.assertEqual(response.status_code, 500)

        self.assertIn('error', response.json())

    def test_rout_does_not_exists(self):
        response = requests.get(f'{self.health_url}2')
        self.assertEqual(response.status_code, 404)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_server.shutdown()
