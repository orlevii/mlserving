import falcon as f

from mest.api import Request
from mest.predictors import RESTPredictor


class InferenceResource:
    def __init__(self, predictor: RESTPredictor):
        self.predictor = predictor

    def on_post(self, req: f.Request, res: f.Response):
        mest_req = Request(req.media, req.headers)

        response = self.predictor.run(mest_req.payload, mest_req)
        res.body = response.text
        res.status = response.status_string

        return res
