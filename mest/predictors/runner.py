from ._base import PredictorBase
from .utils import error_response
from ..api import Request, Response


class PredictorRunner:
    @classmethod
    def run_inference(cls, predictor: PredictorBase, req: Request) -> Response:
        try:
            features = predictor.before_request(req.payload, req)
            if isinstance(features, Response):
                return features

            processed_data = predictor.pre_process(features, req)
            if isinstance(processed_data, Response):
                return processed_data

            prediction = predictor.predict(processed_data, req)
            if isinstance(prediction, Response):
                return prediction

            post_processed = predictor.post_process(prediction, req)
            if isinstance(post_processed, Response):
                return post_processed
            return Response(data=post_processed)
        except Exception as e:
            return error_response(e)
