from abc import ABC
from typing import Optional

from mest.api import Request, validate_schema
from ._base import PredictorBase


class RESTPredictor(PredictorBase, ABC):
    """
    REST predictor, for handling REST requests of inference
    """
    REQUEST_SCHEMA: Optional[dict] = None

    def before_request(self, input_data: dict, req: Request) -> dict:
        if self.REQUEST_SCHEMA is not None:
            input_data = validate_schema(input_data=input_data,
                                         schema=self.REQUEST_SCHEMA)

        return input_data

    def pre_process(self, features: dict, req: Request):
        return features
