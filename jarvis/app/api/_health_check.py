from functools import partial


class HealthCheckStatus(object):
    OK = 'OK'
    ERROR = 'ERROR'


class HealthCheckResult(object):
    def __init__(self, status, message=None):
        self.status = status
        if message:
            self.message = message


class ValidHealthCheck(HealthCheckResult):
    def __init__(self, message=None):
        super().__init__(status=HealthCheckStatus.OK,
                         message=message)


class InvalidHealthCheck(HealthCheckResult):
    def __init__(self, message=None):
        super().__init__(status=HealthCheckStatus.ERROR,
                         message=message)


def generate_models_health_check(models_instances) -> dict:
    health_check_methods = {}
    for model_instance in models_instances:
        model_checker = partial(_check_model, model_instance)
        health_check_methods[type(model_instance).__name__] = model_checker

    return health_check_methods


def _check_model(model_instance, **kwargs):
    return model_instance.health()
