from typing import List

from ._base import PredictorBase
from .runner import PredictorRunner
from ..api import Request, Response


class PipelinePredictor(PredictorBase):
    """
    This class will run a pipeline of predictors.
    Great for chaining models one after the other.
    """
    def __init__(self, predictors: List[PredictorBase]):
        self.predictors = predictors

    def predict(self, processed_data, req: Request):
        # Initialize empty response
        result = Response(data={})
        data = processed_data

        for p in self.predictors:
            result = PredictorRunner.run_inference(p, req, data)
            data = result.data
            if self._is_not_ok(result):
                return result

        return result

    @staticmethod
    def _is_not_ok(res: Response):
        status_code = res.get_status_code()
        return status_code < 200 or status_code > 300
