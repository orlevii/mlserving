from mest.api import Request, request_schema
from mest.app.health import Unhealthy, HealthHandler, HealthStatus
from mest.predictors import RESTPredictor

REQUEST_SCHEMA = {
    "some_required_field": "float"
}


@request_schema(REQUEST_SCHEMA)
class FailPredictor(RESTPredictor):

    def predict(self, processed_data, req: Request):
        return 6.0


class FailHealthHandler(HealthHandler):
    HEALTH_ERROR = 'Unhealthy model...'

    def health_check(self) -> HealthStatus:
        return Unhealthy(self.HEALTH_ERROR)
