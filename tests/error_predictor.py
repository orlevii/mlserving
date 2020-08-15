from mest.api import Request
from mest.app.health import Unhealthy, HealthHandler, HealthStatus
from mest.predictors import RESTPredictor


class FailPredictor(RESTPredictor):
    REQUEST_SCHEMA = {
        'some_required_field': {'type': 'float', 'required': True}
    }

    def predict(self, processed_data, req: Request):
        return 6.0


class FailHealthHandler(HealthHandler):
    HEALTH_ERROR = 'Unhealthy model...'

    def health_check(self) -> HealthStatus:
        return Unhealthy(self.HEALTH_ERROR)
