from mest.api import Response
from mest.models import BaseModel
from mest.predictors import PredictorBase


class MyModel(BaseModel):
    def __init__(self):
        # Could be loaded from files...
        self.weights = [1, 1, 1]

    def func(self, features):
        return sum(features)

    def create_predictor(self):
        return MyPredictor(self)


class MyPredictor(PredictorBase):
    def __init__(self, model):
        super().__init__(model)

    def pre_process(self, input_data: dict):
        # Some pre_processing
        features = [
            input_data.get('feature1', 0) * self.model.weights[0],
            input_data.get('feature2', 0) * self.model.weights[1],
            input_data.get('feature3', 0) * self.model.weights[2]
        ]

        return features

    def infer(self, features) -> float:
        return self.model.func(features)

    def post_process(self, prediction) -> Response:
        return Response(
            data={'score': prediction}
        )
