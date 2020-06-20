from falcon import Request, Response

from mest.models import BaseModel


class InferenceResource:
    def __init__(self, model: BaseModel):
        self.model = model

    def on_post(self, req: Request, res: Response):
        predictor = self.model.create_predictor()

        input_data = req.media
        response = predictor.predict(input_data)

        res.body = response.text
        res.status = response.status_string

        return res
