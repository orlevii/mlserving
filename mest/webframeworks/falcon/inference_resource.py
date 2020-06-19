from falcon import Request, Response
import json


class InferenceResource:
    def __init__(self, predictor_cls, model):
        self.model = model
        self.predictor_cls = predictor_cls

    def on_post(self, req: Request, res: Response):
        predictor = self.predictor_cls(self.model)
        data_str = req.stream.read().decode('utf-8')

        input_data = json.loads(data_str)
        response = predictor.predict(input_data)

        return res
