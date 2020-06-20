import logging
import threading
import unittest
from random import randint, random

import requests

from mest import Mest
from tests.common import create_test_server
from tests.complex_model import MyModel, MyPredictor


class MestFalconTest(unittest.TestCase):
    """Test cases for mest application setup"""
    mest = None
    port = None
    test_server = None
    model = None

    @classmethod
    def setUpClass(cls):
        cls.mest = Mest(framework='falcon')
        cls.mest.logger.setLevel(logging.NOTSET)
        cls.model = MyModel()
        cls.mest.add_health_handler(cls.model, '/api/v1/health')
        cls.mest.add_inference_handler(cls.model, '/api/v1/predict')
        cls.test_server = create_test_server(cls.mest.app)
        cls.port = cls.test_server.server_port
        t = threading.Thread(target=cls.test_server.serve_forever)
        t.start()

    def setUp(self):
        self.health_url = f'http://localhost:{self.port}/api/v1/health'
        self.inference_route = f'http://localhost:{self.port}/api/v1/predict'

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

    @classmethod
    def tearDownClass(cls) -> None:
        cls.test_server.shutdown()
