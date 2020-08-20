from mlserving import ServingApp
from mlserving.api import Request
from mlserving.predictors import RESTPredictor


class MyPredictor(RESTPredictor):

    def __init__(self):
        self.weights = [0.2, 0.1, -0.5]

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

    def post_process(self, prediction, req: Request) -> dict:
        return {
            'score': prediction
        }


app = ServingApp()

app.add_inference_handler('/api/v1/predict', MyPredictor())
app.add_health_handler('/api/v1/ping')

if __name__ == '__main__':
    app.run(port=1234)

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
