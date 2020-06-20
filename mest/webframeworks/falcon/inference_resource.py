from falcon import Request, Response
from mest.models import BaseModel
import json


class InferenceResource:
    def __init__(self, model: BaseModel):
        self.model = model

    def on_post(self, req: Request, res: Response):
        predictor = self.model.create_predictor()
        data_str = req.stream.read().decode('utf-8')

        input_data = json.loads(data_str)
        response = predictor.predict(input_data)

        res.body = response.text
        res.status = response.status_string

        return res
