from mest import Mest
from mest.api import Response
from mest.models import BaseModel
from mest.predictors import BasePredictor


class MyModel(BaseModel):
    def __init__(self):
        # Could be loaded from files...
        self.weights = [0.2, 0.1, -0.5]

    def func(self, features):
        return sum(features)

    def create_predictor(self) -> BasePredictor:
        return MyPredictor(self)


class MyPredictor(BasePredictor):
    def __init__(self, model):
        self.model: MyModel = None
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


mest = Mest()
app = mest.app  # For gunicorn

mest.add_inference_handler(MyModel(), '/api/v1/predict')
mest.add_health_handler(MyModel(), '/api/v1/ping')

if __name__ == '__main__':
    mest.run(port=1234)

# Now, you can run a simple POST request!
"""
curl -X POST http://localhost:1234/api/v1/predict \
-H 'Content-Type: application/json' \
  -d '{
    "feature1": 10,
    "feature2": 4,
    "feature3": 0.123
}'
"""

# health-check?
"""
curl http://localhost:1234/api/v1/ping
"""
