from abc import ABC

from mlserving.api import Request
from mlserving.api.request_validation import RequestValidator
from ._base import PredictorBase


class RESTPredictor(PredictorBase, ABC):
    """
    REST predictor, for handling REST requests of inference
    """

    def before_request(self, input_data: dict, req: Request) -> dict:
        return RequestValidator.validate_schema(type(self), input_data)

    def pre_process(self, features: dict, req: Request):
        return features
