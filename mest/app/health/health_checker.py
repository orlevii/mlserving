import logging
from http import HTTPStatus

from mest.api import Response
from mest.app.state import runtime_state
from .status import Unhealthy


def _full_name(model):
    t = type(model)
    return '{}.{}'.format(t.__module__, t.__name__).strip('.')


class HealthChecker:
    @classmethod
    def run(cls, model: 'BaseModel') -> Response:
        if runtime_state.is_shutting_down():
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                            data={'message': 'Shutting down...'})

        health_status = cls.__model_health(model)

        if not health_status.healthy:
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                            data={
                                'message': health_status.message
                            })

        return Response(data={'message': 'ok'},
                        status=HTTPStatus.OK)

    @staticmethod
    def __model_health(model: 'BaseModel'):
        try:
            return model.health_status()
        except Exception as e:
            logging.getLogger('mest').warning(e)
            return Unhealthy('Could not check model: {}'.format(_full_name(model)))
