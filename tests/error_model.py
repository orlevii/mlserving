from mest.app.health import Unhealthy
from mest.models import BaseModel
from mest.predictors import BasePredictor


class FailModel(BaseModel):
    HEALTH_ERROR = 'Unhealthy model...'

    def create_predictor(self):
        return FailModelPredictor(self)

    def health_status(self):
        return Unhealthy(self.HEALTH_ERROR)


class FailModelPredictor(BasePredictor):
    REQUEST_SCHEMA = {
        'some_required_field': {'type': 'float', 'required': True}
    }

    def __init__(self, model):
        self.model: FailModel = None
        super().__init__(model)

    def infer(self, features) -> float:
        return 6.0
