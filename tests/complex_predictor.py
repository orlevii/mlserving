from mest.api import Response, Request
from mest.api import request_schema
from mest.predictors import RESTPredictor

REQUEST_SCHEMA = {
    'feature1': 'float',
    'feature2': 'float',
    'feature3': 'float'
}


@request_schema(REQUEST_SCHEMA)
class MyPredictor(RESTPredictor):
    def __init__(self):
        self.weights = [1, 1, 1]

    def pre_process(self, input_data: dict, req: Request):
        # Some pre_processing
        features = [
            input_data.get('feature1', 0) * self.weights[0],
            input_data.get('feature2', 0) * self.weights[1],
            input_data.get('feature3', 0) * self.weights[2]
        ]

        return features

    def predict(self, features, req: Request) -> float:
        return sum(features)

    def post_process(self, prediction, req: Request) -> Response:
        return Response(
            data={'score': prediction}
        )
