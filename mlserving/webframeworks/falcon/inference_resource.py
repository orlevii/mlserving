import falcon as f

from mlserving.api import Request
from mlserving.predictors import RESTPredictor
from mlserving.predictors.runner import PredictorRunner


class InferenceResource:
    def __init__(self, predictor: RESTPredictor):
        self.predictor = predictor

    def on_post(self, req: f.Request, res: f.Response):
        mlserving_req = Request(req.media, req.headers)

        response = PredictorRunner.run_inference(self.predictor, mlserving_req)
        res.body = response.text
        res.status = response.status_string

        return res
