from ._base import PredictorBase
from .utils import error_response
from ..api import Request, Response


class PredictorRunner:
    RUN_ORDER = [
        'before_request',
        'pre_process',
        'predict',
        'post_process'
    ]

    @classmethod
    def run_inference(cls, predictor: PredictorBase, req: Request, input_data=None) -> Response:
        try:
            result = input_data
            if input_data is None:
                result = req.payload
            for method_name in cls.RUN_ORDER:
                method = getattr(predictor, method_name)
                result = method(result, req)

                if isinstance(result, Response):
                    return result

            return Response(data=result)
        except Exception as e:
            return error_response(e)
