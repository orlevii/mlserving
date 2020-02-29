import datetime
import json

from flask import Blueprint, current_app

from mest.app._state import runtime_state
from ._request_parser import validate_params


class Router(object):
    def __init__(self, name):
        self._blueprint = Blueprint(name, __name__)

    def route(self, url, method='POST', **options):
        def decorator(func):
            methods = options.pop('methods', [method])

            blueprint_decorator = self._blueprint.route(url, methods=methods, endpoint=func.__name__, **options)

            return blueprint_decorator(func)

        return decorator

    def add_predict_route(self, model_instance, schema, url='/predict', method='POST'):
        @self.route(url, method=method)
        @validate_params(schema=schema)
        def predict(**params):
            try:
                result = model_instance.predict(**params)

                return json.dumps(result)
            except Exception as e:
                response = {'message': str(e)}

                return json.dumps(response), 500

    def add_ping_route(self, url='/ping', method='GET'):
        @self.route(url=url, method=method)
        def ping():
            msg = 'Pong from {}! - {}'.format(current_app.config['MEST'].service_name,
                                              datetime.datetime.now())

            status_code = 503 if runtime_state.is_shutting_down() else 200

            return json.dumps({'message': msg}), status_code
