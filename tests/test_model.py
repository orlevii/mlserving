import random
import unittest

from mest.models import GenericModel
from tests.common import MyTestModel


class MestCoreModelsTest(unittest.TestCase):
    """Test cases for mest application setup"""

    def setUp(self):
        pass

    def test_simple_predict(self):
        expected_result = 'hello_world'
        test_model = MyTestModel()
        test_model.model = expected_result

        result = test_model.predict()

        self.assertEqual(result, expected_result)

    def test_predict_flow1(self):
        model = ModelWithProcessing1()
        model.init(None)
        expected_result = {
            'prediction': 3 * model.model
        }

        result = model.predict(factor=2)

        self.assertEqual(result, expected_result)

    def test_predict_flow2(self):
        model = ModelWithProcessing2()
        model.init(None)
        expected_result = {
            'prediction': 2 + model.model
        }

        result = model.predict(factor=2)

        self.assertEqual(result, expected_result)


class ModelWithProcessing1(GenericModel):
    def init(self, path):
        self.model = random.randint(1, 10)

    def pre_process(self, factor):
        return self.model * factor

    def infer(self, form_pre_process):
        return self.model + form_pre_process

    def post_process(self, prediction):
        return {
            'prediction': prediction
        }


class ModelWithProcessing2(GenericModel):
    def init(self, path):
        self.model = random.randint(1, 10)

    def pre_process(self, factor):
        return [self.model, factor]

    def infer(self, *form_pre_process):
        return {
            'data': sum(form_pre_process)
        }

    def post_process(self, **prediction):
        return {
            'prediction': prediction['data']
        }
