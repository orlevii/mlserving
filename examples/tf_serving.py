from mlserving import ServingApp
from mlserving.api import Request
from mlserving.predictors import RESTPredictor

from mlserving.predictors.tensorflow import TFServingPrediction


class Predictor(TFServingPrediction, RESTPredictor):
    def __init__(self):
        # Initialize TFServingPrediction
        # We don't need to load the tensorflow model here since the inference is done on TensorFlowServing
        super().__init__()
        # TODO: load relevant resources for feature processing

    def pre_process(self, features: dict, req: Request):
        return {
            "instances": [
                # TODO: fill your tensor inputs here
            ]
        }

    def post_process(self, prediction, req: Request):
        prediction = prediction['prediction']
        return {
            'probabilities': prediction,
        }


def main():
    app = ServingApp()
    app.add_inference_handler('/invoke', Predictor())
    app.run()


if __name__ == '__main__':
    main()

"""
Setup tensorflow-serving locally with docker: https://www.tensorflow.org/tfx/serving/docker

docker run -p 8501:8501 \
  --mount type=bind,source=/path/to/my_model/,target=/models/model \
  -e MODEL_NAME=model -t tensorflow/serving
"""
