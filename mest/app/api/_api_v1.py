import datetime
import json

from flask import current_app, Flask

from mest.app._state import runtime_state
from ._router import Router
from ._health_check import ValidHealthCheck, InvalidHealthCheck, HealthCheckStatus


def generate_api_v1() -> Router:
    api_v1 = Router('v1')

    @api_v1.route(url='/ping', method='GET')
    def ping():
        msg = 'Pong from {}! - {}'.format(current_app.config['MEST'].service_name,
                                          datetime.datetime.now())

        return json.dumps({'message': msg})

    @api_v1.route(url='/health', method='GET')
    def health():
        health_info = _get_health_info(current_app)
        errors = [result for result in health_info.values() if result.get('status') == HealthCheckStatus.ERROR]
        has_errors = any(errors)

        service_name = current_app.config['MEST'].service_name
        status = runtime_state.status

        status_code = 503 if runtime_state.is_shutting_down() or has_errors else 200
        response = dict(service_name=service_name,
                        status=status,
                        health=health_info)

        return json.dumps(response), status_code

    return api_v1


def _get_health_info(flask_app: Flask):
    methods = flask_app.config['MEST'].health_check_methods

    statuses = {}
    for method_name, method in methods.items():
        try:
            status = method()
            if status is None:
                status = ValidHealthCheck()

            statuses[method_name] = status.__dict__
        except Exception as err:
            msg = 'Failed to perform health check on "{}"'.format(method_name)
            flask_app.logger.warning(msg)

            status_msg = "{} - {}".format(msg, str(err))
            status = InvalidHealthCheck(message=status_msg)
            statuses[method_name] = status.__dict__

    return statuses
