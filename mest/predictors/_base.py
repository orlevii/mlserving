import abc
from http import HTTPStatus
from typing import Any, Union, Optional

from mest.api import Response, validate_schema


class PredictorBase:
    """
    The base predictor class, orchestrates the prediction flow
    """
    REQUEST_SCHEMA: Optional[dict] = None

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
        if self.REQUEST_SCHEMA is not None:
            input_data = validate_schema(input_data=input_data,
                                         schema=self.REQUEST_SCHEMA)

        return input_data

    def pre_process(self, features: Any) -> Union[Any, Response]:
        return features

    @abc.abstractmethod
    def infer(self, processed_data: Any) -> Union[Any, Response]:
        pass

    def post_process(self, prediction) -> Response:
        return Response(data=prediction)

    @staticmethod
    def error_response(e: Exception):
        return Response(data={'error': str(e)},
                        status=HTTPStatus.INTERNAL_SERVER_ERROR)
