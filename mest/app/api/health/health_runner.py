import json

from flask import current_app

from mest.app._state import runtime_state
from .health_check import HealthCheckStatus
from .health_check import InvalidHealthCheck
from .health_check import ValidHealthCheck


class HealthRunner:
    @classmethod
    def run(cls, health_check_methods):
        health_info = cls.__get_health_info(methods=health_check_methods)
        errors = [result for result in health_info.values() if result.get('status') == HealthCheckStatus.ERROR]
        has_errors = any(errors)

        service_name = current_app.config['MEST'].service_name
        status = runtime_state.status

        status_code = 503 if runtime_state.is_shutting_down() or has_errors else 200
        response = dict(service_name=service_name,
                        status=status,
                        health=health_info)

        return json.dumps(response), status_code

    @staticmethod
    def __get_health_info(methods):
        statuses = {}
        for method_name, method in methods.items():
            try:
                status = method()
                if status is None:
                    status = ValidHealthCheck()

                statuses[method_name] = status.__dict__
            except Exception as err:
                msg = 'Failed to perform health check on "{}"'.format(method_name)
                current_app.logger.warning(msg)

                status_msg = "{} - {}".format(msg, str(err))
                status = InvalidHealthCheck(message=status_msg)
                statuses[method_name] = status.__dict__

        return statuses
