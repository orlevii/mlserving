import logging
import os
from random import randint
from typing import Any, Union
from unittest.mock import MagicMock
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler

from mest.api import Response
from mest.models import BaseModel
from mest.predictors import PredictorBase

logging.getLogger('mest').disabled = True


class MyTestModel(BaseModel):
    def create_predictor(self):
        return MyTestPredictor(self)

    def __init__(self):
        file_path = os.path.join(current_file_path(), '_models', 'model.txt')
        with open(file_path, 'r') as fs:
            self.model = fs.read()


class MyTestPredictor(PredictorBase):
    def __init__(self, model):
        self.model: MyTestModel = None  # Just for type annotation
        super().__init__(model)

    def infer(self, processed_data: Any) -> Union[Any, Response]:
        return self.model.model


def current_file_path():
    return os.path.dirname(os.path.abspath(__file__))


def create_test_server(app):
    port = randint(1000, 9999)
    httpd = simple_server.make_server('0.0.0.0', port, app)
    WSGIRequestHandler.log_message = MagicMock()
    return httpd
