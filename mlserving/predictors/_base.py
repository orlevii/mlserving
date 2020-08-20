import abc
from typing import Union

from mlserving.api import Request, Response


class PredictorBase:
    """
    The base predictor class, orchestrates the prediction flow
    """

    def before_request(self, input_data, req: Request):
        return input_data

    def pre_process(self, features, req: Request):
        return features

    @abc.abstractmethod
    def predict(self, processed_data, req: Request):
        pass

    def post_process(self, prediction, req: Request) -> Union[dict, Response]:
        return prediction
