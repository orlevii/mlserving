import abc
from typing import Union

from mest.api import Request, Response
from mest.predictors.utils import error_response


class PredictorBase:
    """
    The base predictor class, orchestrates the prediction flow
    """

    def run(self, input_data, req: Request) -> Response:
        try:
            features = self.before_request(input_data, req)
            if isinstance(features, Response):
                return features

            processed_data = self.pre_process(features, req)
            if isinstance(processed_data, Response):
                return processed_data

            prediction = self.predict(processed_data, req)
            if isinstance(prediction, Response):
                return prediction

            post_processed = self.post_process(prediction, req)
            if isinstance(post_processed, Response):
                return post_processed
            return Response(data=post_processed)
        except Exception as e:
            return error_response(e)

    def before_request(self, input_data, req: Request):
        return input_data

    def pre_process(self, features, req: Request):
        return features

    @abc.abstractmethod
    def predict(self, processed_data, req: Request):
        pass

    def post_process(self, prediction, req: Request) -> Union[dict, Response]:
        return prediction
