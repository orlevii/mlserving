from mest.app.health import Unhealthy
from mest.models import BaseModel
from mest.predictors import PredictorBase


class FailModel(BaseModel):
    HEALTH_ERROR = 'Unhealthy model...'
    BEFORE_REQUEST_ERROR = 'Could not process input_data'

    def create_predictor(self):
        return FailModelPredictor(self)

    def health_status(self):
        return Unhealthy(self.HEALTH_ERROR)


class FailModelPredictor(PredictorBase):
    def __init__(self, model):
        self.model: FailModel = None
        super().__init__(model)

    def before_request(self, input_data: dict):
        raise RuntimeError(self.model.BEFORE_REQUEST_ERROR)

    def infer(self, features) -> float:
        return 6.0
