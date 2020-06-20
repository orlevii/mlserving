from http import HTTPStatus
from typing import List

from mest.api import Response
from mest.app.state import runtime_state
from mest.models import BaseModel


def __full_name(model: BaseModel):
    t = type(model)
    return '{}.{}'.format(t.__module__, t.__name__).strip('.')


def get_app_health(models: List[BaseModel]) -> Response:
    if runtime_state.is_shutting_down():
        return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                        data={'message': 'Shutting down...'})

    unhealthy_models = [__full_name(m)
                        for m in models
                        if not m.is_healthy]
    if any(unhealthy_models):
        return Response(status=HTTPStatus.SERVICE_UNAVAILABLE,
                        data={
                            'message': 'Unhealthy models: {}'.format(', '.join(unhealthy_models))
                        })

    return Response(status=HTTPStatus.OK)
