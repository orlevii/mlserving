import datetime
import json

from flask import current_app, Flask

from mest.app._state import runtime_state
from ._router import Router
from .health.health_check import ValidHealthCheck, InvalidHealthCheck, HealthCheckStatus


def generate_api_v1() -> Router:
    api_v1 = Router('v1')

    return api_v1



