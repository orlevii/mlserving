import logging
from http import HTTPStatus

from mlserving.api import Response
from mlserving._state import runtime_state
from .health_handler import HealthHandler
from .status import Unhealthy


def _full_name(health_checker):
    t = type(health_checker)
    return '{}.{}'.format(t.__module__, t.__name__).strip('.')


class HealthCheckRunner:
    @classmethod
    def run(cls, health_checker: HealthHandler) -> Response:
        if runtime_state.is_shutting_down():
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                            data={'message': 'Shutting down...'})

        health_status = cls.__get_health(health_checker)

        if not health_status.healthy:
            return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                            data={
                                'message': health_status.message
                            })

        return Response(data={'message': 'ok'},
                        status=HTTPStatus.OK)

    @staticmethod
    def __get_health(health_checker: HealthHandler):
        try:
            return health_checker.health_check()
        except Exception as e:
            logging.getLogger('mlserving').warning(e)
            return Unhealthy(f'Could not health-check: {_full_name(health_checker)}')
