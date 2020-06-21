import abc
from http import HTTPStatus
from typing import Any, Union

from mest.api import Response


class PredictorBase:
    def __init__(self, model):
        self.model = model

    def predict(self, input_data) -> Response:
        try:
            features = self.before_request(input_data)
            if isinstance(features, Response):
                return features

            processed_data = self.pre_process(features)
            if isinstance(processed_data, Response):
                return processed_data

            prediction = self.infer(processed_data)
            if isinstance(prediction, Response):
                return prediction

            return self.post_process(prediction)
        except Exception as e:
            return self.error_response(e)

    def before_request(self, input_data: dict) -> Union[Any, Response]:
        return input_data

    def pre_process(self, features: Any) -> Union[Any, Response]:
        return features

    @abc.abstractmethod
    def infer(self, processed_data: Any) -> Union[Any, Response]:
        pass

    def post_process(self, prediction) -> Response:
        return Response(data=prediction)

    def error_response(self, e: Exception):
        return Response(data={'error': str(e)},
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)
